from PIL import Image
import numpy as np

def load_gif_frames(path):
    gif = Image.open(path)
    frames = []

    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_rgba = gif.convert("RGBA")
        frames.append(np.array(frame_rgba))

    return frames
