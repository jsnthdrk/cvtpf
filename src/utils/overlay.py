import cv2
import numpy as np

def overlay_rgba(background, overlay, x, y):
    """
    Desenha um RGBA sobre um BGR (background) com recorte seguro nas bordas.
    Não crasha mesmo se parte da imagem ficar fora da tela.
    """
    bg_h, bg_w = background.shape[:2]
    h, w = overlay.shape[:2]

    # Se está completamente fora, não faz nada
    if x >= bg_w or y >= bg_h or x + w <= 0 or y + h <= 0:
        return

    # Área de interseção no background
    x1 = max(x, 0)
    y1 = max(y, 0)
    x2 = min(x + w, bg_w)
    y2 = min(y + h, bg_h)

    # Área correspondente no overlay
    ov_x1 = x1 - x
    ov_y1 = y1 - y
    ov_x2 = ov_x1 + (x2 - x1)
    ov_y2 = ov_y1 + (y2 - y1)

    overlay_crop = overlay[ov_y1:ov_y2, ov_x1:ov_x2]

    if overlay_crop.size == 0:
        return

    alpha = overlay_crop[:, :, 3] / 255.0
    rgb = overlay_crop[:, :, :3]

    bg_region = background[y1:y2, x1:x2]

    if bg_region.shape[:2] != alpha.shape:
        return  # segurança extra

    blended = (alpha[..., None] * rgb + (1 - alpha[..., None]) * bg_region).astype(np.uint8)
    background[y1:y2, x1:x2] = blended
