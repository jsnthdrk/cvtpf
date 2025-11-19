import cv2

def cast_mage_hand(frame):
    cv2.putText(frame, "Mage Hand conjured!", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

def cast_fireball(frame):
    cv2.putText(frame, "Fireball!", (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 50, 255), 3)
    
def cast_book_buff(frame):
    cv2.putText(frame, "Spellbook Detected! +INT", (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
