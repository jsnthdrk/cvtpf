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
    hand_size = dist(lm[0], lm[9])
    if hand_size == 0:
        return None
    
    # hand_big = dist(lm[0], lm[9]) > 0.20  - old
    # -------------------------------
    # funções helpers
    # -------------------------------
    def normalized_dist(p1, p2):
        return dist(p1, p2) / hand_size

    def is_curled(tip, pip): 
        return lm[tip].y - lm[pip].y * hand_size > 0.0 # - consistencia de sinal

    def is_extended(tip, pip): 
        return not is_curled(tip, pip)

    
    # ================================
    # Lógica de detecção de gestos
    # ================================
    # SHIELD
    # ================================
    hand_big = hand_size > 0.2 # valor experimental
    front_facing = normalized_dist(lm[0], lm[9]) < 0.35 # palma de frente
    curled_fingers = sum([
        is_curled(8,6),   # indicador (não considerar 5, porque =index_finger_mcp)*
        is_curled(12,10), # dedo do meio (não considerar 9, porque =middle_finger_mcp)*
        is_curled(16,14), # anelar (não considerar 13, porque =ring_finger_mcp)*
        is_curled(20,18)  # mindinho (não considerar 17, porque =pinky_finger_mcp)*
        # xx_xxx_mcp -> landmarks que representam a base dos dedos (metacarpal tubercule), ou seja, a parte da mão onde os dedos se conectam à palma.
    ])
    
    if hand_big and front_facing and curled_fingers >= 2:
        return "SHIELD"

    # ================================
    # PINCH
    # ================================
    thumb_index_close = normalized_dist(thumb, index) < 0.3
    index_extended = lm[8].y < lm[6].y
    if thumb_index_close and index_extended:
        return "PINCH"

    # ================================
    # HEAL
    # ================================
    thumb_index_close = normalized_dist(thumb, middle) < 0.3
    thumb_index_far = normalized_dist(thumb, index) > 0.35
    if thumb_index_close and thumb_index_far:
        return "HEAL"

    # ================================
    # OPEN → fireball
    # ================================
    open_fingers = sum([
        # (nao consideramos o valor de mcp como descrito no metodo de SHIELD)
        is_extended(8,6),   # indicador
        is_extended(12,10), # dedo do meio
        is_extended(16,14), # anelar
        is_extended(20,18)  # mindinho
    ])
    if open_fingers >= 3:
        return "OPEN"
    
    return None