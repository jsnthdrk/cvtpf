import math

def dist(p1, p2):
    return math.dist([p1.x, p1.y], [p2.x, p2.y])

def detect_gesture(hands):
    """
    DETECTA:
    - LIGHTNING  (2 mãos)
    - SHIELD     (1 mão grande + palma de frente + dedos dobrados)
    - PINCH      (polegar + indicador)
    - HEAL       (polegar + dedo do meio)
    - OPEN       (mão aberta)
    """

    # ================================
    # SEM MÃO
    # ================================
    if not hands or len(hands) == 0:
        return None

    # ================================
    # LIGHTNING = 2 mãos visíveis
    # ================================
    if len(hands) >= 2:
        return "LIGHTNING"

    # ================================
    # ANALISAR A ÚNICA MÃO
    # ================================
    hand = hands[0]
    lm = hand.landmark

    # ---- conveniências ----
    thumb  = lm[4]
    index  = lm[8]
    middle = lm[12]
    ring   = lm[16]
    pinky  = lm[20]

    # ---- Tamanho da mão: mede pulso até centro da palma ----
    hand_big = dist(lm[0], lm[9]) > 0.20  

    # ---- Palma voltada pra camera ----
    front_facing = abs(lm[0].x - lm[9].x) < 0.06

    # ---- Dedos dobrados ----
    def curled(tip, pip): return lm[tip].y > lm[pip].y
    curled_fingers = sum([
        curled(8,6), curled(12,10), curled(16,14), curled(20,18)
    ])

    # ================================
    # SHIELD
    # ================================
    if hand_big and front_facing and curled_fingers >= 2:
        return "SHIELD"

    # ================================
    # PINCH
    # ================================
    thumb_index_close = dist(thumb, index) < 0.06
    index_extended = lm[8].y < lm[6].y

    if thumb_index_close and index_extended:
        return "PINCH"

    # ================================
    # HEAL
    # ================================
    if dist(thumb, middle) < 0.06 and dist(thumb, index) > 0.07:
        return "HEAL"

    # ================================
    # OPEN → fireball
    # ================================
    def extended(tip, pip): return lm[tip].y < lm[pip].y
    open_fingers = sum([
        extended(8,6),
        extended(12,10),
        extended(16,14),
        extended(20,18)
    ])

    if open_fingers >= 3:
        return "OPEN"

    return None
