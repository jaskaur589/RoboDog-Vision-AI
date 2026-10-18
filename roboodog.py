
import cv2
import numpy as np
import time



cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    raise SystemExit

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("RoboDog Vision AI started!")
print("Show an ORANGE ball to the camera.")
print("Press Q to quit.")



width = 640
height = 480

lower_orange = np.array([0, 80, 50])
upper_orange = np.array([30, 255, 255])

min_area = 300
stop_threshold = 50000

left_boundary = width // 3
right_boundary = 2 * width // 3

# WOOF message settings
found_before = False
woof_start_time = 0
woof_duration = 2



while True:

    ret, frame = cap.read()

    if not ret or frame is None:
        print("Could not read webcam frame.")
        break

    frame = cv2.resize(frame, (width, height))
    frame = cv2.flip(frame, 1)

   

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(
        hsv,
        lower_orange,
        upper_orange
    )

    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN, kernel
    )

    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE, kernel
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    command = "BALL NOT FOUND"
    ball_detected = False

    

    if contours:

        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area > min_area:

            ball_detected = True

            x, y, w, h = cv2.boundingRect(largest)

            cx = x + w // 2
            cy = y + h // 2

            box_area = w * h

            # Draw green bounding box
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Draw blue centre point
            cv2.circle(
                frame,
                (cx, cy),
                6,
                (255, 0, 0),
                -1
            )


            if not found_before:
                print("WOOF! Orange ball detected!")
                woof_start_time = time.time()

            found_before = True

         

            if box_area > stop_threshold:
                command = "STOP"

            elif cx < left_boundary:
                command = "TURN LEFT"

            elif cx < right_boundary:
                command = "GO STRAIGHT"

            else:
                command = "TURN RIGHT"

            cv2.putText(
                frame,
                "ORANGE BALL DETECTED",
                (10, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Centre: ({cx}, {cy})",
                (10, height - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Area: {box_area}",
                (10, 135),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

  
    if not ball_detected:
        found_before = False

    

    cv2.line(
        frame,
        (left_boundary, 0),
        (left_boundary, height),
        (255, 255, 255),
        1
    )

    cv2.line(
        frame,
        (right_boundary, 0),
        (right_boundary, height),
        (255, 255, 255),
        1
    )

  

    command_color = (
        (0, 0, 255) if command == "STOP"
        else (0, 255, 0)
    )

    cv2.rectangle(
        frame,
        (0, 0),
        (width, 50),
        (30, 30, 30),
        -1
    )

    cv2.putText(
        frame,
        command,
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        command_color,
        2
    )

 

    if (
        ball_detected
        and time.time() - woof_start_time < woof_duration
    ):
        cv2.putText(
            frame,
            "WOOF! BALL DETECTED!",
            (10, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )


    cv2.imshow("RoboDog Vision AI", frame)
    cv2.imshow("Orange Detection Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()

print("RoboDog stopped.")
