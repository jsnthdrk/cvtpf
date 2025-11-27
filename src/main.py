import cv2
import numpy as np
from pipeline.hands import HandTracker
from pipeline.gestures import detect_gesture
from pipeline.yolo import ObjectDetector
from utils.gif_loader import load_gif_frames
from utils.overlay import overlay_rgba
from PIL import Image
import spells

# LOAD ASSETS
def load_png(path):
    try:
        return np.array(Image.open(path).convert("RGBA"))
    except:
        print(f"❌ Erro ao carregar PNG: {path}")
        return None

png_hand = load_png("assets/mage-hand.png")
png_shield = load_png("assets/shield.png")

gif_fire = load_gif_frames("assets/fire-ball.gif")
gif_heal = load_gif_frames("assets/heal.gif")

# INIT
tracker = HandTracker()
detector = ObjectDetector()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    yolo_result = detector.detect(frame)
    annotated = yolo_result.plot()

    results = tracker.process(frame)

    if not results.multi_hand_landmarks:
        cv2.putText(annotated, "NO HAND DETECTED", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    else:
        hand = results.multi_hand_landmarks[0]
        gesture = detect_gesture(hand)

        cv2.putText(annotated, f"Gesture: {gesture}", (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if gesture == "PINCH":
            spells.cast_static_spell(annotated, png_hand, pos=(300, 250))

        elif gesture == "OPEN":
            spells.cast_animated_spell(annotated, gif_fire, key="fire", pos=(200, 200))

    cv2.imshow("D&D AR", annotated)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
