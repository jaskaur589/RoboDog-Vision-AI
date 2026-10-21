
import cv2
import numpy as np

# 1. Open the laptop webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam.")
    print("Try changing VideoCapture(0) to VideoCapture(1).")
    raise SystemExit

# Camera display dimensions
width = 640
height = 360

# Divide the screen into three regions
left_boundary = width // 3
right_boundary = 2 * width // 3

# Orange ball HSV colour range
lower_orange = np.array([5, 140, 50])
upper_orange = np.array([25, 255, 255])

# Detection settings
area_threshold = 100
stop_threshold = 18000
found_before = False

print("RoboDog Vision AI started!")
print("Show an orange ball to the webcam.")
print("Press Q to quit.")

while True:
    # 2. Capture one live webcam frame
    ret, frame = cap.read()

    if not ret:
        print("Could not read webcam frame.")
        break

    frame = cv2.resize(frame, (width, height))

    # 3. Convert BGR image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 4. Keep only orange pixels
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # 5. Find connected orange regions
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    command = "BALL NOT FOUND"

    if contours:
        # Select the largest orange region
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area > area_threshold:
            # 6. Find the bounding box
            x, y, w, h = cv2.boundingRect(largest)

            # Calculate the centre
            cx = x + w // 2
            cy = y + h // 2

            # Draw green bounding box and blue centre point
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.circle(
                frame,
                (cx, cy),
                5,
                (255, 0, 0),
                -1
            )

            # 7. WOOF when the ball is first detected
            if not found_before:
                print("WOOF! Ball detected!")
                found_before = True

            # 8. Choose RoboDog's command
            box_area = w * h

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
                "WOOF! BALL DETECTED!",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Centre: ({cx}, {cy})",
                (10, height - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

    # 9. Display the current command
    cv2.putText(
        frame,
        command,
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # Draw left, centre and right boundaries
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

    # 10. Show the live processed frame
    cv2.imshow("RoboDog Vision AI", frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 11. Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()

print("RoboDog stopped.")
