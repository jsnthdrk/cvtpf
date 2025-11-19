import cv2
from pipeline.hands import HandTracker
from pipeline.gestures import detect_gesture
from pipeline.yolo import ObjectDetector
import spells

tracker = HandTracker()
detector = ObjectDetector()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # YOLO detection
    yolo_result = detector.detect(frame)
    annotated = yolo_result.plot()

    # MediaPipe hands
    results = tracker.process(frame)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        gesture = detect_gesture(hand)

        if gesture == "PINCH":
            spells.cast_mage_hand(annotated)

        elif gesture == "OPEN":
            spells.cast_fireball(annotated)

    cv2.imshow("D&D AR Spells - MVP", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
