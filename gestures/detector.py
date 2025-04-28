def detect_gesture(hand_landmarks):
    lm = hand_landmarks.landmark
    index_finger = lm[8]
    thumb = lm[4]
    middle = lm[12]
    pinky = lm[20]
    palm = lm[0]

    # Dynamic cursor gesture (thumb far from index)
    if abs(index_finger.x - thumb.x) > 0.1:
        return "MOUSE_MOVE", index_finger
    # Screenshot Gesture
    elif abs(index_finger.x - thumb.x) > 0.2:
        return "SCREENSHOT", None
    # Volume Up
    elif pinky.y < palm.y and middle.y < palm.y:
        return "VOLUME_UP", None
    # Volume Down
    elif pinky.y > palm.y and middle.y > palm.y:
        return "VOLUME_DOWN", None
    # Click gesture
    elif abs(index_finger.x - thumb.x) < 0.03:
        return "CLICK", index_finger
    else:
        return "NONE", None
