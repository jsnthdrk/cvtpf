import cv2
import numpy as np
from utils.overlay import overlay_rgba

_animation_idx = {}

def next_idx(key, frames):
    if key not in _animation_idx:
        _animation_idx[key] = 0
    idx = _animation_idx[key] % len(frames)
    _animation_idx[key] += 1
    return idx

def scale_to_height(img, target_h):
    h, w = img.shape[:2]
    scale = target_h / float(h)
    new_w = int(w * scale)
    return cv2.resize(img, (new_w, target_h), interpolation=cv2.INTER_AREA)

# ========================================
# 🔥 FIREBALL (igual antes)
# ========================================
def cast_fireball(frame, frames, center):
    if not frames: return
    fh, fw, _ = frame.shape
    img = scale_to_height(frames[next_idx("fire",frames)], int(fh*0.18))
    h, w = img.shape[:2]
    x = center[0] - w//2
    y = center[1] - h//2
    overlay_rgba(frame, img, x, y)

# ========================================
# ✋ MAGE HAND
# ========================================
def cast_mage_hand(frame, png, center):
    if png is None: return
    fh = frame.shape[0]
    img = scale_to_height(png, int(fh*0.22))
    h, w = img.shape[:2]
    overlay_rgba(frame, img, center[0]-w//2, center[1]-h//2)

# ========================================
# ⚡ LIGHTNING → TELA CHEIA
# ========================================
def cast_lightning_fullscreen(frame, frames):
    if not frames: return
    fh, fw, _ = frame.shape

    # usa o frame inteiro
    img = cv2.resize(frames[next_idx("lightning", frames)], (fw, fh))
    overlay_rgba(frame, img, 0, 0)

# ========================================
# 💚 HEAL
# ========================================
def cast_heal(frame, frames, center):
    if not frames: return
    fh = frame.shape[0]
    img = scale_to_height(frames[next_idx("heal",frames)], int(fh*0.20))
    h, w = img.shape[:2]
    overlay_rgba(frame, img, center[0]-w//2, center[1]-h//2)

# ========================================
# 🛡 SHIELD → tampando antebraço
# ========================================
def cast_shield(frame, png, wrist, palm):
    if png is None: return
    fh = frame.shape[0]

    # Big shield
    img = scale_to_height(png, int(fh*0.55))

    cx = (wrist[0] + palm[0])//2
    cy = (wrist[1] + palm[1])//2 - int(fh*0.05)

    h, w = img.shape[:2]
    overlay_rgba(frame, img, cx-w//2, cy-h//2)
