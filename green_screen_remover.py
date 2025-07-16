import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
from PIL import Image
import os
import datetime

# =========================
# CONFIGURABLE PARAMETERS
# =========================
GREEN_LOWER = np.array([40, 100, 50])   # HSV lower bound for green
GREEN_UPPER = np.array([80, 255, 255])  # HSV upper bound for green
FEATHER_RADIUS = 15                     # Edge feathering (must be odd)
SPILL_SUPPRESS = 0.7                    # Spill suppression strength

# =========================
# INPUT/OUTPUT PATHS
# =========================
INPUT_VIDEO = 0  # 0 for webcam, or path to video file
BACKGROUND_IMAGE = "background/background.jpg"  # Path to background image
BACKGROUND_VIDEO = "background.mp4"  # Path to background video (optional)
RECORDING_FOLDER = "recording"
SNAPSHOT_FOLDER = "snapshot"

# Ensure output directories exist
os.makedirs(RECORDING_FOLDER, exist_ok=True)
os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)

# =========================
# ADVANCED CHROMA KEY FUNCTION
# =========================
def advanced_chroma_key(frame, bg, green_lower, green_upper, feather_radius=15, spill_suppress=0.7):
    """
    Perform advanced chroma keying with soft masking and color decontamination.
    Returns the composited frame with the background replaced.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create a soft mask for green areas
    mask = cv2.inRange(hsv, green_lower, green_upper).astype(np.float32) / 255.0
    mask = cv2.GaussianBlur(mask, (feather_radius, feather_radius), 0)
    mask = np.clip(mask, 0, 1)
    # Morphological cleanup
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    # Color decontamination (reduce green spill)
    frame_no_spill = frame.copy().astype(np.float32)
    green = frame_no_spill[..., 1]
    red_blue = (frame_no_spill[..., 0] + frame_no_spill[..., 2]) / 2
    spill_mask = (green > red_blue) & (mask > 0.05)
    frame_no_spill[..., 1][spill_mask] = red_blue[spill_mask] * (1 - spill_suppress) + frame_no_spill[..., 1][spill_mask] * spill_suppress
    # Alpha blend with background
    mask_3c = np.stack([mask]*3, axis=-1)
    result = frame_no_spill * (1 - mask_3c) + bg.astype(np.float32) * mask_3c
    return result.astype(np.uint8)

# =========================
# UTILITY FUNCTIONS
# =========================
def load_background(bg_path, frame_shape):
    """Load and resize background image to match frame size."""
    bg = Image.open(bg_path).convert("RGB")
    bg = bg.resize((frame_shape[1], frame_shape[0]))
    return np.array(bg)[:, :, ::-1]  # Convert RGB to BGR

def get_audio_from_video(video_path):
    """Extract audio from video file."""
    return AudioFileClip(video_path)

# =========================
# MAIN APPLICATION LOGIC
# =========================
def main():
    # Open video input (webcam or file)
    cap = cv2.VideoCapture(INPUT_VIDEO)
    if not cap.isOpened():
        print("Error: Cannot open video source.")
        return

    # Read first frame to get shape
    ret, frame = cap.read()
    if not ret:
        print("Error: Cannot read from video source.")
        return
    frame_shape = frame.shape
    bg_img = load_background(BACKGROUND_IMAGE, frame_shape)
    bg_vid_cap = None
    if BACKGROUND_VIDEO:
        bg_vid_cap = cv2.VideoCapture(BACKGROUND_VIDEO)

    # Prepare output video writer with unique timestamp
    TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # type: ignore
    OUTPUT_VIDEO = os.path.join(RECORDING_FOLDER, f"output_{TIMESTAMP}.mp4")
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, cap.get(cv2.CAP_PROP_FPS), (frame_shape[1], frame_shape[0]))

    # Live preview and background toggle
    bg_mode = 0  # 0: image, 1: video, 2: black
    print("Press 'b' to toggle background, 'q' to quit, 's' to save frame.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Select background
        if bg_mode == 0:
            bg = bg_img
        elif bg_mode == 1 and bg_vid_cap:
            ret_bg, bg = bg_vid_cap.read()
            if not ret_bg or bg is None:
                bg_vid_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret_bg, bg = bg_vid_cap.read()
            if not ret_bg or bg is None:
                print("Warning: Could not read background video frame. Using black background.")
                bg = np.zeros_like(frame)
            else:
                bg = cv2.resize(bg, (frame_shape[1], frame_shape[0]))
        else:
            bg = np.zeros_like(frame)
        # Advanced chroma keying
        result = advanced_chroma_key(frame, bg, GREEN_LOWER, GREEN_UPPER, FEATHER_RADIUS, SPILL_SUPPRESS)
        # Show preview
        cv2.imshow("Green Screen Remover", result)
        # Write to output
        out.write(result)
        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('b'):
            bg_mode = (bg_mode + 1) % 3
        elif key == ord('s'):
            snap_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_path = os.path.join(SNAPSHOT_FOLDER, f"snapshot_{snap_timestamp}.png")
            cv2.imwrite(snapshot_path, result)
            print(f"Snapshot saved at {snapshot_path}.")
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    # Attach audio if input is a video file
    if isinstance(INPUT_VIDEO, str):
        print("Attaching audio...")
        video_clip = VideoFileClip(OUTPUT_VIDEO)
        audio_clip = get_audio_from_video(INPUT_VIDEO)
        final_output_path = os.path.join(RECORDING_FOLDER, f"final_output_{TIMESTAMP}.mp4")
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(final_output_path, codec="libx264", audio_codec="aac")
        print(f"Exported with audio as {final_output_path}")

if __name__ == "__main__":
    main()