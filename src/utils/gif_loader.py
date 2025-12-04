from PIL import Image                    # Usado para abrir GIFs e acessar frames individuais
import numpy as np                       # Converte frames para arrays manipuláveis pelo OpenCV


def load_gif_frames(path):
    # Abre o arquivo GIF usando PIL
    # Image.open não carrega tudo de uma vez — apenas inicializa o objeto
    gif = Image.open(path)

    # Lista final onde guardaremos cada frame convertido para RGBA (numpy)
    frames = []

    # Percorre todos os frames existentes no GIF
    # gif.n_frames = atributo que diz quantos frames existem no arquivo
    for frame in range(gif.n_frames):

        # seek() move o cursor interno do GIF para o frame solicitado
        # (PIL não "descompacta" todos os frames automaticamente)
        gif.seek(frame)

        # Converte o frame atual para RGBA
        # Isso garante que teremos canal alpha, necessário para overlay
        frame_rgba = gif.convert("RGBA")

        # Converte o frame RGBA do PIL para um array NumPy (H, W, 4)
        # Cada pixel vira [R, G, B, A]
        frames.append(np.array(frame_rgba))

    # Retorna a lista completa — cada item é um frame RGBA independente
    return frames
