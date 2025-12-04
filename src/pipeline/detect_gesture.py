import math   # Usado para math.hypot, que calcula distância Euclidiana com precisão


# ============================================================
# Distância 2D entre dois pontos de landmark
# ============================================================
def dist2d(a, b):
    # math.hypot(dx, dy) = sqrt(dx² + dy²)
    # Usa valores normalizados de landmark (entre 0 e 1)
    return math.hypot(a.x - b.x, a.y - b.y)



# ============================================================
# FUNÇÃO PRINCIPAL DE DETECÇÃO DE GESTOS
# ============================================================
def detect_gesture(hands):

    # Se não existe nenhuma mão detectada → não há gesto
    if not hands or len(hands) == 0:
        return None

    # Número de mãos detectadas neste frame
    num = len(hands)



    # ============================================================
    # Helpers internos para lógica dos dedos
    # (usam apenas coordenada Y, pois dedo estendido = Y do tip < Y da junta)
    # ============================================================

    def extended(lm, tip, pip):
        # Dedo estendido = ponta do dedo está MAIS ACIMA (menor Y)
        return lm[tip].y < lm[pip].y

    def curled(lm, tip, pip):
        # Dedo dobrado = ponta do dedo está MAIS ABAIXO (maior Y)
        return lm[tip].y > lm[pip].y



    # Conta quantos dedos estão estendidos
    def fingers_extended(lm):
        return sum([
            extended(lm, 8, 6),    # indicador
            extended(lm, 12, 10),  # médio
            extended(lm, 16, 14),  # anelar
            extended(lm, 20, 18),  # mindinho
        ])

    # Conta quantos dedos estão fechados/dobrados
    def fingers_curled(lm):
        return sum([
            curled(lm, 8, 6),      # indicador
            curled(lm, 12, 10),    # médio
            curled(lm, 16, 14),    # anelar
            curled(lm, 20, 18),    # mindinho
        ])



    # ============================================================
    # 1) GESTOS QUE USAM AS 2 MÃOS (PRIORIDADE ABSOLUTA)
    # ============================================================
    if num >= 2:
        lm1 = hands[0].landmark     # landmarks da mão 1
        lm2 = hands[1].landmark     # landmarks da mão 2

        # Coordenada Y do pulso (landmark 0)
        # Menor Y = mais alto na imagem
        w1_y = lm1[0].y
        w2_y = lm2[0].y

        # Define se cada mão está "levantada"
        # threshold 0.90 é permissivo, pois Y é normalizado
        up1 = w1_y < 0.90
        up2 = w2_y < 0.90

        # Conta dedos estendidos (>=3 = palma aberta)
        open1 = fingers_extended(lm1) >= 3
        open2 = fingers_extended(lm2) >= 3

        # Conta dedos fechados (>=3 = punho)
        fist1 = fingers_curled(lm1) >= 3
        fist2 = fingers_curled(lm2) >= 3

        # Distância horizontal entre as palmas (lm[9] = centro da palma)
        cx1 = lm1[9].x
        cx2 = lm2[9].x

        # Se estão relativamente próximas horizontalmente
        close = abs(cx1 - cx2) < 0.35

        # ========================================================
        # LIGHTNING
        # ========================================================
        # Condição: duas palmas abertas levantadas
        if up1 and up2 and open1 and open2:
            return "LIGHTNING"

        # ========================================================
        # SHIELD
        # ========================================================
        # Condição: dois punhos fechados, mãos levantadas, próximas
        if up1 and up2 and fist1 and fist2 and close:
            return "SHIELD"

        # Se tem 2 mãos mas não formam nenhum gesto reconhecível
        return None



    # ============================================================
    # 2) GESTOS DE UMA MÃO
    # ============================================================

    lm = hands[0].landmark     # Landmark da mão única

    # Mede o tamanho "base" da mão (pulso → palma)
    # usado como normalização de distâncias
    size = dist2d(lm[0], lm[9]) or 1.0   # evita divisão por zero

    # ========================================================
    # PINCH → polegar tocando indicador + indicador estendido
    # ========================================================
    if dist2d(lm[4], lm[8]) / size < 0.25 and extended(lm, 8, 6):
        return "PINCH"

    # ========================================================
    # HEAL → indicador estendido, médio estendido,
    #        anelar dobrado, mindinho dobrado (sinal de V)
    # ========================================================
    if (
        extended(lm, 8, 6) and
        extended(lm, 12, 10) and
        curled(lm, 16, 14)  and
        curled(lm, 20, 18)
    ):
        return "HEAL"

    # ========================================================
    # FIREBALL / OPEN → 3 ou mais dedos estendidos
    # ========================================================
    if fingers_extended(lm) >= 3:
        return "OPEN"

    # Nenhum gesto reconhecido
    return None
