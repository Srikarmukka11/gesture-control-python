import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from filterpy.kalman import KalmanFilter

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize Kalman Filter
kf = KalmanFilter(dim_x=4, dim_z=2)
kf.x = np.array([0, 0, 0, 0])  # initial state (position and velocity)
kf.F = np.array([[1, 0, 1, 0],
                 [0, 1, 0, 1],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]])  # state transition matrix
kf.H = np.array([[1, 0, 0, 0],
                 [0, 1, 0, 0]])  # Measurement function
kf.P *= 1000.  # covariance matrix
kf.R = np.array([[10, 0],
                 [0, 10]])  # measurement noise
kf.Q = np.eye(4)  # process noise

# Get screen size
screen_w, screen_h = pyautogui.size()

# Capture video
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7,
                    min_tracking_confidence=0.7,
                    max_num_hands=1) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Flip and convert the image color
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(image_rgb)

        # Draw hand landmarks
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Get index finger tip landmark (landmark 8)
                x = hand_landmarks.landmark[8].x
                y = hand_landmarks.landmark[8].y

                # Map the coordinates
                screen_x = np.interp(x, [0, 1], [0, screen_w])
                screen_y = np.interp(y, [0, 1], [0, screen_h])

                # Kalman filter prediction and update
                kf.predict()
                kf.update(np.array([screen_x, screen_y]))
                smooth_x, smooth_y = kf.x[0], kf.x[1]

                # Move the mouse
                pyautogui.moveTo(smooth_x, smooth_y, duration=0.01)

                # Draw the landmarks
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Show the image
        cv2.imshow('Kalman Gesture Control', image)

        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
