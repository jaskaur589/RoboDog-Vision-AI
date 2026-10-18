# RoboDog Vision AI

A real-time computer vision project built using Python and OpenCV.

## Features
- Detects an orange ball using HSV colour thresholding.
- Identifies the ball using contours.
- Draws a bounding box and centre point.
- Divides the camera view into left, centre, and right regions.
- Generates `TURN LEFT`, `GO STRAIGHT`, `TURN RIGHT`, and `STOP` commands.
- Displays a temporary WOOF message when the ball is newly detected.

## Technologies
- Python
- OpenCV
- NumPy

## Setup

Install the required libraries:

```bash
python -m pip install -r requirements.txt
```

Run the project:

```bash
python roboodog.py
```

Press **Q** to exit.

## Notes
The project currently generates vision-based commands; it does not directly control physical robot motors. The STOP command uses the detected bounding-box size as a rough proximity estimate.
# RoboDog-Vision-AI
Real-time orange ball detection and vision-based movement commands using Python and OpenCV.
