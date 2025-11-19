import math

def distance(p1, p2):
    return math.dist([p1.x, p1.y], [p2.x, p2.y])

def detect_gesture(hand_landmarks):
    thumb = hand_landmarks.landmark[4]
    index = hand_landmarks.landmark[8]

    # Gesto 1: Pinça
    if distance(thumb, index) < 0.07:
        return "PINCH"

    # Gesto 2: Palma aberta
    fingers_extended = [
        hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y,
        hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y,
        hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y,
        hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y,
    ]

    if sum(fingers_extended) >= 3:
        return "OPEN"

    return None
