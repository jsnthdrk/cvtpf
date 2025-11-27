from utils.overlay import overlay_rgba

animation_indices = {}

def cast_static_spell(frame, img, pos=(0, 0)):
    if img is None:
        return
    overlay_rgba(frame, img, pos[0], pos[1])

def cast_animated_spell(frame, frames, key="default", pos=(0, 0)):
    if not frames:
        return

    if key not in animation_indices:
        animation_indices[key] = 0

    idx = animation_indices[key] % len(frames)
    overlay_rgba(frame, frames[idx], pos[0], pos[1])
    animation_indices[key] += 1
