import math

def dist(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y) # distancia euclidiana corrigida

def detect_gesture(hands):
    """
    DETECTA:
    - LIGHTNING  : (2 mãos)
    - SHIELD     : mão grande singular com a palma da frente e mais de 2 dedos dobrados
    - PINCH      : polegar + indicador (polegar perto do indicador e o indicador estendido)
    - HEAL       : sinal de "V" (polegar perto do dedo médio e longe do indicador) | teve que ser mudado face ao que está presente na proposta incial devido a problemas de deteção
    - OPEN       : 3 ou mais dedos estendidos
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
    # aqui vamos usar a primeira mão detetada para gestos de 1 mão
    # ================================
    hand = hands[0]
    lm = hand.landmark

    # ---- conveniências (valor inicial) ----
    thumb  = lm[4]
    index  = lm[8]
    middle = lm[12]
    ring   = lm[16]
    pinky  = lm[20]
    wrist = lm[0]
    palm_center = lm[9]

    # ---- Tamanho da mão: mede pulso até centro da palma ----
    hand_size = dist(wrist, palm_center)
    if hand_size == 0:
        return None
    
    # normalizações
    def normalized_dist(p1, p2):
        return dist(p1, p2) / hand_size

    def is_curled(tip_idx, pip_idx, margin=0.0): 
        return lm[tip_idx].y > lm[pip_idx].y + margin

    def is_extended(tip_idx, pip_idx, margin=0.0): 
        return lm[tip_idx].y > lm[pip_idx].y + margin

    
    # ================================
    # Lógica de detecção de gestos
    # ================================
    # SHIELD
    # ================================
    hand_big = hand_size > 0.18 # valor empirico (podemos ajustar se necessário)
    palm_x_dist = abs(wrist.x - palm_center.x)
    front_facing = palm_x_dist < (hand_size * 0,45)
    curled_fingers = sum([
        is_curled(index,6),   # indicador (não considerar 5, porque =index_finger_mcp)*
        is_curled(middle,10), # dedo do meio (não considerar 9, porque =middle_finger_mcp)*
        is_curled(ring,14), # anelar (não considerar 13, porque =ring_finger_mcp)*
        is_curled(pinky,18)  # mindinho (não considerar 17, porque =pinky_finger_mcp)*
        # xx_xxx_mcp -> landmarks que representam a base dos dedos (metacarpal tubercule), ou seja, a parte da mão onde os dedos se conectam à palma.
    ])
    
    if hand_big and front_facing and curled_fingers >= 2:
        return "SHIELD"

    # ================================
    # PINCH
    # ================================
    thumb_index_norm = normalized_dist(thumb, index)
    index_extended = is_extended(8,6)
    if thumb_index_norm < 0.25 and index_extended:
        return "PINCH"

    # ================================
    # HEAL
    # ================================
    def is_v_sign():
        return (
            is_extended(8,6, margin=0.0) and
            is_extended(12,10, margin=0.0) and
            is_curled(16,14, margin=0.0) and
            is_curled(20,18, margin=0.0)
        )
        
    if is_v_sign():
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
    
    # se nenhum gesto for detetado
    return None