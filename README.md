# <p align="center">✨AI Powered Green Screen Remover✨</p>
<!-------------------------------------------------------------------------------------------------------------------------------------->
<div align="center">
<p>

[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
![Visitors](https://api.visitorbadge.io/api/visitors?path=harshal0212%2FGreen-Screen-Remover%20&countColor=%23263759&style=flat)
![GitHub contributors](https://img.shields.io/github/contributors/harshal0212/Green-Screen-Remover)
![GitHub last commit](https://img.shields.io/github/last-commit/harshal0212/Green-Screen-Remover)
![GitHub repo size](https://img.shields.io/github/repo-size/harshal0212/Green-Screen-Remover)
![GitHub total lines](https://sloc.xyz/github/harshal0212/Green-Screen-Remover)

</p>
</div>

<!-- --------------------------------------------------------------------------------------------------------------------------------------------------------- -->

An advanced, real-time green screen remover and background replacer using Python, OpenCV, and MoviePy. Supports webcam or video input, live background toggling, and high-quality chroma keying with spill suppression and edge feathering.

## Features
- Real-time or video file input
- Advanced chroma keying (soft masking, spill suppression, edge feathering)
- Automatic background resizing and blending
- Toggle between image, video, or black backgrounds live
- Save recordings and snapshots with unique filenames
- Export with audio preservation (for video files)

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-powered-green-screen.git
   cd ai-powered-green-screen
   ```
2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Mac/Linux
   ```
3. **Install dependencies:**
   ```bash
   pip install opencv-python numpy pillow moviepy
   ```
4. **Add your background image:**
   - Place your background image at `background/background.jpg` (create the folder if needed).
   - (Optional) Add a background video as `background.mp4`.

## Usage
Run the script:
```bash
python green_screen_remover.py
```

### Controls
- `b` — Toggle background (image, video, black)
- `q` — Quit
- `s` — Save a snapshot (saved in `snapshot/` folder)

### Output
- Recordings are saved in the `recording/` folder with unique timestamps.
- Snapshots are saved in the `snapshot/` folder with unique timestamps.
- If using a video file as input, the final output with audio is also saved in `recording/`.

## Notes
- For best results, use even lighting and a solid green background.
- You can tune the chroma key parameters in the script for your setup.

## License
MIT 
