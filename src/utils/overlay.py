import cv2
import numpy as np

def overlay_rgba(background, overlay, x, y):
    """
    Desenha um RGBA sobre um BGR com recorte seguro nas bordas.
    """

    # Pega altura e largura do background (frame da câmera)
    bg_h, bg_w = background.shape[:2]     # Ex: (480, 640)

    # Pega altura e largura do overlay (sprite RGBA)
    h, w = overlay.shape[:2]              # Ex: (128, 128)

    # --- TESTE DE LIMITE TOTAL ---
    # Se o overlay está completamente fora da tela,
    # não há nada para desenhar → retorna sem erro.
    if x >= bg_w or y >= bg_h or x + w <= 0 or y + h <= 0:
        return

    # --- CALCULA REGIÃO VISÍVEL DENTRO DO BACKGROUND ---
    # x1, y1 = canto superior na tela onde o overlay realmente aparece
    x1 = max(x, 0)                        # Se x é negativo, recorta para 0 (borda esquerda)
    y1 = max(y, 0)                        # Se y é negativo, recorta para 0 (borda superior)

    # x2, y2 = canto inferior recortado, impedindo passar das bordas
    x2 = min(x + w, bg_w)                # Limita à borda direita
    y2 = min(y + h, bg_h)                # Limita à borda inferior

    # --- CALCULA REGIÃO QUE VEM DO OVERLAY ---
    # Converte coordenadas da região visível do BG
    # para a região equivalente dentro da imagem overlay.
    ov_x1 = x1 - x                        # Se o overlay começou fora, isso vira positivo
    ov_y1 = y1 - y
    ov_x2 = ov_x1 + (x2 - x1)             # Define o recorte exato na largura
    ov_y2 = ov_y1 + (y2 - y1)             # Define o recorte exato na altura

    # Recorte final do overlay (parte que realmente aparece na tela)
    overlay_crop = overlay[ov_y1:ov_y2, ov_x1:ov_x2]

    # Se por algum motivo não sobrar área válida, sai
    if overlay_crop.size == 0:
        return

    # Extrai canal alpha como float entre 0 e 1
    alpha = overlay_crop[:, :, 3] / 255.0  # Matriz shape (H, W)

    # Extrai apenas os canais RGB do sprite
    rgb = overlay_crop[:, :, :3]           # Matriz shape (H, W, 3)

    # Recorta a região correspondente do background para aplicar o blend
    bg_region = background[y1:y2, x1:x2]   # Mesma shape do recorte do overlay

    # Segurança: se tamanhos não casarem, aborta
    if bg_region.shape[:2] != alpha.shape:
        return

    # --- BLENDING ---
    # Fórmula:
    # final = alpha * sprite_rgb + (1 - alpha) * background_bgr
    blended = (
        alpha[..., None] * rgb +           # Aplica alpha para cada canal RGB
        (1 - alpha[..., None]) * bg_region # Parte do background que aparece atrás do sprite
    ).astype(np.uint8)                     # Converte de float para uint8 (0–255)

    # Coloca a região blendada de volta no background
    background[y1:y2, x1:x2] = blended     # Substitui somente a área necessária
