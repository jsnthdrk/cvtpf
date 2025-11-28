import math

def dist(p1, p2):
    return math.dist([p1.x, p2.y], [p1.y, p2.y])

def detect_gesture(hands):
    """
    Gestos:
    - LIGHTNING  → 2 mãos
    - SHIELD     → 1 mão grande + palma de frente + dedos dobrados
    - PINCH      → mage hand
    - HEAL       → thumb + middle
    - OPEN       → fireball
    """
    if not hands:
        return None

    # -------------------------
    # LIGHTNING = 2 MÃOS
    # -------------------------
    if len(hands) >= 2:
        return "LIGHTNING"

    # -------------------------
    # ANALISAR SOMENTE UMA MÃO
    # -------------------------
    hand = hands[0]
    lm = hand.landmark

    # tamanho da mão na imagem
    hand_big = dist(lm[0], lm[9]) > 0.20    # antes era 0.25 (ajustei)

    # palma de frente
    front_facing = abs(lm[0].x - lm[9].x) < 0.06

    # dedos dobrados
    def curled(tip, pip): return lm[tip].y > lm[pip].y
    curled_fingers = sum([
        curled(8,6), curled(12,10), curled(16,14), curled(20,18)
    ])

    # -------------------------
    # SHIELD
    # -------------------------
    if hand_big and front_facing and curled_fingers >= 2:
        return "SHIELD"

    # -------------------------
    # PINCH
    # -------------------------
    thumb = lm[4]
    index = lm[8]
    thumb_index_close = dist(thumb, index) < 0.06
    index_extended = lm[8].y < lm[6].y
    if thumb_index_close and index_extended:
        return "PINCH"

    # -------------------------
    # HEAL
    # -------------------------
    def is_v_sign():
        index_extended = lm[8].y < lm[6].y
        middle_extended = lm[12].y < lm[10].y
        ring_folded = lm[16].y > lm[14].y
        pinky_folded = lm[20].y > lm[18].y
        
        return index_extended and middle_extended and ring_folded and pinky_folded
    
    if is_v_sign():
        return "HEAL"

    # -------------------------
    # OPEN
    # -------------------------
    def extended(tip,pip): return lm[tip].y < lm[pip].y
    open_fingers = sum([
        extended(8,6), extended(12,10), extended(16,14), extended(20,18)
    ])

    if open_fingers >= 3:
        return "OPEN"

    return None
