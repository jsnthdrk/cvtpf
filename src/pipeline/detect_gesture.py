import math

def dist2d(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def detect_gesture(hands):
    if not hands or len(hands) == 0:
        return None

    num = len(hands)

    # helpers
    def extended(lm, tip, pip):
        return lm[tip].y < lm[pip].y

    def curled(lm, tip, pip):
        return lm[tip].y > lm[pip].y

    def fingers_extended(lm):
        return sum([
            extended(lm, 8, 6),
            extended(lm, 12, 10),
            extended(lm, 16, 14),
            extended(lm, 20, 18),
        ])

    def fingers_curled(lm):
        return sum([
            curled(lm, 8, 6),
            curled(lm, 12, 10),
            curled(lm, 16, 14),
            curled(lm, 20, 18),
        ])

    # ============================================================
    # 1) GESTOS DE 2 MÃOS (têm prioridade absoluta)
    # ============================================================
    if num >= 2:
        lm1 = hands[0].landmark
        lm2 = hands[1].landmark

        w1_y = lm1[0].y
        w2_y = lm2[0].y

        # Mãos levantadas (muito permissivo)
        up1 = w1_y < 0.90
        up2 = w2_y < 0.90

        open1 = fingers_extended(lm1) >= 3
        open2 = fingers_extended(lm2) >= 3

        fist1 = fingers_curled(lm1) >= 3
        fist2 = fingers_curled(lm2) >= 3

        cx1 = lm1[9].x
        cx2 = lm2[9].x
        close = abs(cx1 - cx2) < 0.35

        # LIGHTNING (duas palmas abertas levantadas)
        if up1 and up2 and open1 and open2:
            return "LIGHTNING"

        # SHIELD (duas mãos fechadas levantadas próximas)
        if up1 and up2 and fist1 and fist2 and close:
            return "SHIELD"

        # Se há 2 mãos mas não batem lightning/shield
        return None

    # ============================================================
    # 2) GESTOS DE UMA MÃO
    # ============================================================
    lm = hands[0].landmark

    size = dist2d(lm[0], lm[9]) or 1.0

    if dist2d(lm[4], lm[8]) / size < 0.25 and extended(lm, 8, 6):
        return "PINCH"

    if (
        extended(lm, 8, 6) and
        extended(lm, 12, 10) and
        curled(lm, 16, 14) and
        curled(lm, 20, 18)
    ):
        return "HEAL"

    if fingers_extended(lm) >= 3:
        return "OPEN"

    return None
