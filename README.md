# RoboDog Vision AI

A real-time computer vision project that detects an orange ball using Python and OpenCV.

## Features
- Detects an orange ball using HSV color filtering.
- Draws a bounding box around the detected ball.
- Tracks the ball's center.
- Generates movement commands: TURN LEFT, GO STRAIGHT, TURN RIGHT, and STOP.
- Displays WOOF when the ball is newly detected.

## Technologies
- Python
- OpenCV
- NumPy

## Installation

Install the required libraries:

```bash
python -m pip install -r requirements.txt
```

## Run the project

```bash
python roboodog.py
```

Press **Q** to quit.

## Note
This project generates vision-based movement commands. It does not currently control physical robot motors. The STOP command uses the detected ball's bounding-box area as a rough proximity estimate.
