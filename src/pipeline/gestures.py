import math

def distance(p1, p2):
    return math.dist([p1.x, p1.y], [p2.x, p2.y])

def detect_gesture(hand_landmarks):
    # Proteção contra landmarks inválidos
    if not hand_landmarks or not hand_landmarks.landmark:
        return None

    lm = hand_landmarks.landmark

    # Proteção contra mão detectada parcialmente
    if len(lm) < 21:
        return None

    thumb = lm[4]
    index = lm[8]

    # Gesto 1 — Pinça
    try:
        if distance(thumb, index) < 0.07:
            return "PINCH"
    except:
        return None

    # Gesto 2 — Mão aberta
    fingers_extended = [
        lm[8].y < lm[6].y,
        lm[12].y < lm[10].y,
        lm[16].y < lm[14].y,
        lm[20].y < lm[18].y,
    ]

    if sum(fingers_extended) >= 3:
        return "OPEN"

    return None
