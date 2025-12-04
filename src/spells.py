import cv2                       # OpenCV, usado para redimensionar e manipular imagens
import numpy as np               # NumPy, usado porque sprites são arrays RGBA
from utils.overlay import overlay_rgba   # Overlay customizado que faz blending RGBA sobre frame BGR


# ============================================================
#   ÍNDICES GLOBAIS PARA ANIMAÇÕES (GIF FRAME COUNTERS)
# ============================================================

_animation_idx = {}              # Armazena, para cada animação, qual frame deve ser exibido no próximo ciclo


def next_idx(key: str, frames: list) -> int:
    # Se nunca usamos essa animação antes, inicializamos seu contador
    if key not in _animation_idx:
        _animation_idx[key] = 0  # Começa do frame zero

    # O frame a ser usado = contador atual modulo quantidade de frames
    # Isso garante looping infinito da animação sem precisar resetar manualmente
    idx = _animation_idx[key] % len(frames)

    # Avança o contador para a próxima iteração
    _animation_idx[key] += 1

    # Retorna o índice que deve ser usado NA renderização atual
    return idx



# ============================================================
#   UTILITÁRIO PARA REDIMENSIONAR IMAGE RGBA
# ============================================================

def scale_to_height(img: np.ndarray, target_h: int) -> np.ndarray:
    # Pega as dimensões originais da imagem (height, width)
    h, w = img.shape[:2]

    # Calcula o fator de escala necessário para que a nova altura seja target_h
    # scale = target_h / h
    scale = target_h / float(h)

    # A nova largura é proporcional ao scale (mantém aspect ratio)
    new_w = int(w * scale)

    # Retorna a imagem redimensionada usando interpolação INTER_AREA (boa para redução)
    return cv2.resize(img, (new_w, target_h), interpolation=cv2.INTER_AREA)



# ============================================================
#   FIREBALL
# ============================================================

def cast_fireball(frame: np.ndarray, frames: list, center: tuple[int, int]):
    # Se não há frames (gif não carregou), aborta
    if not frames:
        return

    # fh = altura do frame da câmera
    fh = frame.shape[0]

    # Seleciona o frame correto da animação com base no contador global
    anim_frame = frames[next_idx("fire", frames)]

    # Redimensiona a fireball para 18% da altura total da tela
    img = scale_to_height(anim_frame, int(fh * 0.18))

    # Pega dimensões do sprite redimensionado
    h, w = img.shape[:2]

    # Calcula onde posicionar o sprite centralizado na palma da mão
    x = center[0] - w // 2
    y = center[1] - h // 2

    # Desenha o sprite sobre o frame da câmera aplicando RGBA → BGR blending
    overlay_rgba(frame, img, x, y)



# ============================================================
#   MAGE HAND
# ============================================================

def cast_mage_hand(frame: np.ndarray, png: np.ndarray, center: tuple[int, int]):
    # Se o PNG não foi carregado, não faz nada
    if png is None:
        return

    # Altura total do frame da câmera
    fh = frame.shape[0]

    # Escala a imagem da mão etérea para 22% da tela
    img = scale_to_height(png, int(fh * 0.22))

    # Dimensões do sprite
    h, w = img.shape[:2]

    # Centraliza o sprite no ponto da palma
    x = center[0] - w // 2
    y = center[1] - h // 2

    # Faz overlay com alpha
    overlay_rgba(frame, img, x, y)



# ============================================================
#   LIGHTNING — Tela Cheia
# ============================================================

def cast_lightning_fullscreen(frame: np.ndarray, frames: list):
    # Se não existe gif carregado, sai
    if not frames:
        return

    # Pega altura e largura do frame da câmera
    fh, fw = frame.shape[:2]

    # Seleciona frame da animação
    anim_frame = frames[next_idx("lightning", frames)]

    # Ajusta o frame do gif para cobrir completamente a tela da webcam
    lightning_img = cv2.resize(anim_frame, (fw, fh))

    # Desenha a animação sobre o frame inteiro (posição 0,0)
    overlay_rgba(frame, lightning_img, 0, 0)



# ============================================================
#   HEAL
# ============================================================

def cast_heal(frame: np.ndarray, frames: list, center: tuple[int, int]):
    # Se não há animação disponível, retorna
    if not frames:
        return

    # Altura do frame da câmera
    fh = frame.shape[0]

    # Seleciona próximo frame do GIF
    anim_frame = frames[next_idx("heal", frames)]

    # Escala para 20% da altura da tela
    img = scale_to_height(anim_frame, int(fh * 0.20))

    # Pega dimensões do sprite redimensionado
    h, w = img.shape[:2]

    # Centraliza na palma
    x = center[0] - w // 2
    y = center[1] - h // 2

    # Faz overlay com alpha
    overlay_rgba(frame, img, x, y)



# ============================================================
#   SHIELD — Antebraço
# ============================================================

def cast_shield(
    frame: np.ndarray,
    png: np.ndarray,
    wrist: tuple[int, int],
    palm: tuple[int, int],
):
    # Se o PNG do escudo falhou ao carregar, sai
    if png is None:
        return

    # Pega altura do frame (usado para definir tamanho do escudo)
    fh = frame.shape[0]

    # Escala o escudo para 55% da altura da tela — grande para cobrir o antebraço
    img = scale_to_height(png, int(fh * 0.55))

    # Cálculo da posição:
    # - cx e cy ficam exatamente no meio entre o pulso e a palma
    # - Isso alinha o escudo com o antebraço
    cx = (wrist[0] + palm[0]) // 2
    cy = (wrist[1] + palm[1]) // 2

    # Eleva Y levemente para que o escudo pareça estar “na frente do braço”
    cy -= int(fh * 0.05)

    # Dimensões do escudo redimensionado
    h, w = img.shape[:2]

    # Centraliza o escudo na posição alvo
    x = cx - w // 2
    y = cy - h // 2

    # Desenha o escudo com alpha blending
    overlay_rgba(frame, img, x, y)
