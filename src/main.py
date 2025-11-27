import cv2
import numpy as np
from PIL import Image

from pipeline.hands import HandTracker
from pipeline.gestures import detect_gesture
from pipeline.yolo import ObjectDetector
from utils.gif_loader import load_gif_frames
import spells

# ==========================
#     LOAD PNG & GIF ASSETS
# ==========================

def load_png(path):
    try:
        return np.array(Image.open(path).convert("RGBA"))
    except Exception as e:
        print(f"❌ Erro ao carregar PNG {path}: {e}")
        return None

print("\n🔄 Carregando assets...")

png_mage   = load_png("assets/mage-hand.png")
png_shield = load_png("assets/shield.png")

gif_fire   = load_gif_frames("assets/fire-ball.gif")
gif_heal   = load_gif_frames("assets/heal.gif")

try:
    gif_light = load_gif_frames("assets/lightning.gif")
except Exception:
    gif_light = []

print("✅ Assets carregados.\n")

# ==========================
#     INIT YOLO + HANDS
# ==========================

tracker = HandTracker()
detector = ObjectDetector()
cap = cv2.VideoCapture(0)

last_gesture = None
stable_count = 0
final_gesture = None

def get_palm_px(lm, w, h):
    return int(lm[9].x * w), int(lm[9].y * h)

def get_wrist_px(lm, w, h):
    return int(lm[0].x * w), int(lm[0].y * h)

# ==========================
#          MAIN LOOP
# ==========================

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ ERRO: câmera não retornou frame.")
        break

    yolo_result = detector.detect(frame)
    annotated = yolo_result.plot()

    results = tracker.process(frame)
    
    # testagem dos landmarks - refinamento
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # desenhar para debug
            tracker.drawer.draw_landmarks(
                annotated,
                hand_landmarks,
                tracker.connections,
                tracker.drawer.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                tracker.drawer.DrawingSpec(color=(0, 0, 255), thickness=2)
            )

    h, w = annotated.shape[:2]

    if not results.multi_hand_landmarks:
        cv2.putText(annotated, "NO HAND DETECTED", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        final_gesture = None
        stable_count = 0

    else:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark

        wrist = get_wrist_px(lm, w, h)
        palm  = get_palm_px(lm, w, h)
        center = palm

        gesture = detect_gesture(results.multi_hand_landmarks)


        # Debounce: só aceita gesto se repetir 3 frames seguidos
        if gesture == last_gesture:
            stable_count += 1
        else:
            stable_count = 0
        last_gesture = gesture

        if stable_count >= 3:
            final_gesture = gesture

        cv2.putText(annotated, f"Gesto: {final_gesture}", (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # ==============================
        #        SPELL ROUTING
        # ==============================

        if final_gesture == "PINCH":
            spells.cast_mage_hand(annotated, png_mage, center)

        elif final_gesture == "OPEN":
            spells.cast_fireball(annotated, gif_fire, center)

        elif final_gesture == "LIGHTNING":
            spells.cast_lightning_fullscreen(annotated, gif_light)

        elif final_gesture == "HEAL":
            spells.cast_heal(annotated, gif_heal, center)

        elif final_gesture == "SHIELD":
            spells.cast_shield(annotated, png_shield, wrist, palm)

    cv2.imshow("D&D AR Spells", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("\n👋 Encerrado.")
