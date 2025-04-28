import cv2
import time
import numpy as np
import pyautogui
import mediapipe as mp
import math
import os

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

# Variables
pTime = 0
frame_count = 0
gesture_counter = {}
GESTURE_CONFIRM_FRAMES = 3
screen_width, screen_height = pyautogui.size()

def fingers_up(hand_landmarks):
    """Return which fingers are up"""
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers
    for id in range(1,5):
        if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def detect_gesture(fingers):
    """Identify gesture based on fingers array"""
    total_fingers = fingers.count(1)

    # Move Mouse
    if fingers == [0,1,0,0,0]:
        return 'MoveMouse'

    # Left Click
    if fingers[1] == 1 and fingers[0] == 1:
        return 'LeftClick'

    # Volume Up
    if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 1:
        return 'VolumeUp'

    # Volume Down
    if fingers == [0,0,0,0,1]:
        return 'VolumeDown'

    # Screenshot
    if total_fingers == 5:
        return 'Screenshot'

    # Lock Screen
    if total_fingers == 0:
        return 'LockScreen'

    # Sleep Mode
    if total_fingers == 5 and fingers[0] == 0:
        return 'Sleep'

    # Launch Chrome
    if fingers == [1,1,0,0,0]:
        return 'LaunchApp'

    return None

def trigger_action(gesture):
    """Trigger specific action based on gesture"""
    if gesture == 'LeftClick':
        pyautogui.click()

    elif gesture == 'VolumeUp':
        pyautogui.press("volumeup")

    elif gesture == 'VolumeDown':
        pyautogui.press("volumedown")

    elif gesture == 'Screenshot':
        pyautogui.screenshot('screenshot.png')
        print("[INFO] Screenshot Taken")

    elif gesture == 'LockScreen':
        os.system('rundll32.exe user32.dll,LockWorkStation')

    elif gesture == 'Sleep':
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

    elif gesture == 'LaunchApp':
        os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')  # Change path if needed
        print("[INFO] Chrome Launched")

while True:
    success, img = cap.read()
    frame_count += 1

    # Process every 2nd frame only
    if frame_count % 2 != 0:
        continue

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            fingers = fingers_up(handLms)
            detected = detect_gesture(fingers)

            if detected:
                gesture_counter[detected] = gesture_counter.get(detected, 0) + 1
                if gesture_counter[detected] >= GESTURE_CONFIRM_FRAMES:
                    print(f"[ACTION] {detected}")
                    trigger_action(detected)
                    gesture_counter = {}  # Reset after action
            else:
                gesture_counter = {}

            # Move Mouse - special case
            if detect_gesture(fingers) == 'MoveMouse':
                index_finger_tip = handLms.landmark[8]
                x = int(index_finger_tip.x * 1280)
                y = int(index_finger_tip.y * 720)

                screen_x = np.interp(x, (100, 1180), (0, screen_width))
                screen_y = np.interp(y, (100, 620), (0, screen_height))

                pyautogui.moveTo(screen_x, screen_y, duration=0.1)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # FPS Counter
    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime != pTime else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
