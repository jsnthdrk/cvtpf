import cv2
import numpy as np

def overlay_rgba(background, overlay, x, y):
    h, w = overlay.shape[:2]

    bg_h, bg_w = background.shape[:2]

    # Impedir estouro para fora
    if x >= bg_w or y >= bg_h:
        return

    w = min(w, bg_w - x)
    h = min(h, bg_h - y)

    overlay = overlay[0:h, 0:w]

    alpha = overlay[:, :, 3] / 255.0
    rgb = overlay[:, :, :3]

    bg_region = background[y:y+h, x:x+w]

    blended = (alpha[..., None] * rgb + (1 - alpha[..., None]) * bg_region).astype(np.uint8)
    background[y:y+h, x:x+w] = blended
