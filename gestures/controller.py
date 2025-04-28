import pyautogui
import os
import time
from ctypes import windll

screen_w, screen_h = pyautogui.size()
last_action_time = 0
cooldown = 1.5  # seconds

def perform_action(gesture, finger_pos=None):
    global last_action_time

    if gesture == "MOUSE_MOVE" and finger_pos:
        x = int(finger_pos.x * screen_w)
        y = int(finger_pos.y * screen_h)
        pyautogui.moveTo(x, y, duration=0.1)
    elif gesture == "CLICK":
        pyautogui.click()
    elif gesture == "VOLUME_UP":
        pyautogui.press("volumeup")
    elif gesture == "VOLUME_DOWN":
        pyautogui.press("volumedown")
    elif gesture == "SCREENSHOT":
        pyautogui.screenshot("screenshot.png")
    elif gesture == "LOCK_SCREEN":
        windll.user32.LockWorkStation()
    elif gesture == "SLEEP_MODE":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif gesture == "LAUNCH_APP":
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

    if gesture != "MOUSE_MOVE":
        print(f"Gesture detected: {gesture}")
        last_action_time = time.time()
