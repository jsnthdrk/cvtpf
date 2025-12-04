import cv2                                   # Biblioteca principal para capturar vídeo, desenhar texto e manipular matriz de pixels
import numpy as np                            # Usada para manipular arrays (imagens carregadas em RGBA)
from PIL import Image                          # Usada para carregar PNGs corretamente mantendo canal alpha

from pipeline.hands import HandTracker          # Classe que encapsula o Mediapipe Hands (rastreamento de mãos)
from pipeline.detect_gesture import detect_gesture  # Função que recebe landmarks e retorna o nome do gesto
from pipeline.yolo import ObjectDetector        # Classe que encapsula modelo YOLO para detectar objetos no frame
from utils.gif_loader import load_gif_frames    # Função que carrega GIF e devolve frames RGBA isolados
import spells                                   # Módulo contendo todas as funções de renderização de magias


# ===================================================================
#  LOAD PNG / GIF ASSETS
# ===================================================================

def load_png(path):
    """
    Carrega o arquivo PNG mantendo o canal alpha.
    """
    try:
        return np.array(                        # Converte a imagem PIL para matriz NumPy (RGBA)
            Image.open(path).convert("RGBA")    # Abre o PNG e converte explicitamente para RGBA
        )
    except Exception as e:
        print(f"Erro ao carregar PNG {path}: {e}")  # Caso o arquivo não exista ou esteja corrompido
        return None


print("\nCarregando assets...")                 # Mensagem de debug

# Cada PNG é carregado com alpha
png_mage   = load_png("assets/mage-hand.png")   # Mão espectral
png_shield = load_png("assets/shield.png")      # Escudo

# Cada GIF retorna uma lista de frames RGBA
gif_fire   = load_gif_frames("assets/fire-ball.gif")
gif_heal   = load_gif_frames("assets/heal.gif")

# Carrega lightning, mas pode falhar dependendo da estrutura interna do GIF
try:
    gif_light = load_gif_frames("assets/lightning.gif")
except Exception:
    gif_light = []                              # Se falhar, substitui por lista vazia para evitar crash

print("Assets carregados.\n")                   # Fim do carregamento visual



# ===================================================================
#  INITIALIZAÇÃO DE YOLO e MEDIAPIPE HANDS
# ===================================================================

tracker  = HandTracker()                        # Instancia o Mediapipe Hands: detecção + rastreamento
detector = ObjectDetector()                     # Instancia YOLO para objetos
cap      = cv2.VideoCapture(0)                  # Abre a webcam (0 = câmera padrão)

# Variáveis usadas para estabilizar o gesto detectado
last_gesture  = None                            # Último gesto detectado no frame anterior
stable_count  = 0                               # Quantos frames consecutivos o mesmo gesto apareceu
final_gesture = None                            # Gesto final validado após estabilidade



# ===================================================================
#  FUNÇÕES AUXILIARES PARA COORDENADAS
# ===================================================================

def get_palm_px(lm, w, h):
    """
    Recebe landmarks normalizados e converte o ponto da palma para pixels.
    """
    return int(lm[9].x * w), int(lm[9].y * h)   # landmark 9 = centro da palma


def get_wrist_px(lm, w, h):
    """
    Converte landmark do pulso (0) para pixel.
    """
    return int(lm[0].x * w), int(lm[0].y * h)



# ===================================================================
#  MAIN LOOP DO SISTEMA DE RA
# ===================================================================

while True:                                     # Loop principal (executa até pressionar ESC)
    ret, frame = cap.read()                     # Captura um frame da webcam
    if not ret:                                 # Se falhar, provavelmente a webcam não está disponível
        print("Erro: câmera não retornou frame.")
        break

    # ============================ YOLO ============================
    # Executa detecção de objetos no frame atual
    yolo_result = detector.detect(frame)

    # Plota bounding boxes e labels diretamente sobre uma cópia do frame
    annotated   = yolo_result.plot()

    # ======================== MEDIA PIPE HANDS ======================
    results = tracker.process(frame)             # Detecta e rastreia as mãos no frame
    h, w = annotated.shape[:2]                   # Dimensões do frame anotado



    # ============================================================
    #  CASO 1 — Nenhuma mão detectada
    # ============================================================
    if not results.multi_hand_landmarks:         # Se lista vazia → nenhuma mão detectada
        cv2.putText(
            annotated,
            "NO HAND DETECTED",                  # Texto de aviso
            (20, 40),                             # Posição na tela
            cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 0, 255), 2                       # Vermelho
        )

        final_gesture = None                     # Reseta gesto final
        stable_count  = 0                        # Reseta estabilização

    # ============================================================
    #  CASO 2 — Mão(s) detectada(s)
    # ============================================================
    else:

        # ------------------------------------------------------
        # Desenhar os landmarks de todas as mãos detectadas
        # ------------------------------------------------------
        for hand_landmarks in results.multi_hand_landmarks:
            tracker.drawer.draw_landmarks(        # Função do Mediapipe para debugar a mão
                annotated,                       # Desenha em annotated (não no frame original)
                hand_landmarks,                  # Estrutura de landmarks da mão
                tracker.connections,             # Conexões padrão (linhas entre dedos)
                tracker.drawer.DrawingSpec(      # Cor dos pontos (verde)
                    color=(0, 255, 0), thickness=2, circle_radius=3
                ),
                tracker.drawer.DrawingSpec(      # Cor das linhas (vermelho)
                    color=(0, 0, 255), thickness=2
                )
            )

        # ------------------------------------------------------
        # Primeira mão detectada → usada para gestos de 1 mão
        # ------------------------------------------------------
        main_hand = results.multi_hand_landmarks[0]  # Seleciona a mão principal
        lm = main_hand.landmark                      # Lista com 21 landmarks normalizados

        # Converte pulso e palma para coordenadas reais de pixel
        wrist  = get_wrist_px(lm, w, h)
        palm   = get_palm_px(lm, w, h)
        center = palm                                # Centro para efeitos que seguem a mão

        # Visualização do pulso (debug)
        cv2.circle(annotated, wrist, 5, (255, 0, 0), -1)  # Desenha um ponto azul no pulso



        # ------------------------------------------------------
        #  DETECÇÃO DE GESTO
        # ------------------------------------------------------
        gesture = detect_gesture(results.multi_hand_landmarks)  # Passa todas as mãos para a detecção



        # ------------------------------------------------------
        #  DEBOUNCE / ESTABILIZAÇÃO
        # ------------------------------------------------------
        if gesture == last_gesture:                 # Se o gesto atual é igual ao anterior
            stable_count += 1                       # Conta mais um frame igual
        else:
            stable_count = 0                        # Reset se gesto mudou

        last_gesture = gesture                      # Atualiza gesto anterior

        if stable_count >= 3:                       # Se gesto repetiu 3 frames seguidos
            final_gesture = gesture                 # Agora ele é "válido"



        # Escreve nome do gesto atual na tela
        cv2.putText(
            annotated,
            f"Gesto: {final_gesture}",
            (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 1,
            (255, 255, 255), 2
        )



        # ============================================================
        #  PRIORIDADE ABSOLUTA: LIGHTNING
        # ============================================================
        if final_gesture == "LIGHTNING":
            spells.cast_lightning_fullscreen(annotated, gif_light)  # Efeito ocupa a tela inteira
            cv2.imshow("D&D AR Spells", annotated)

            # ESC para sair
            if cv2.waitKey(1) & 0xFF == 27:
                break

            continue                       # Ignora qualquer outra magia neste frame



        # ============================================================
        #  SEGUNDA PRIORIDADE: SHIELD
        # ============================================================
        if final_gesture == "SHIELD":
            spells.cast_shield(annotated, png_shield, wrist, palm)



        # ============================================================
        #  GESTOS DE UMA MÃO
        # ============================================================
        elif final_gesture == "PINCH":
            spells.cast_mage_hand(annotated, png_mage, center)

        elif final_gesture == "HEAL":
            spells.cast_heal(annotated, gif_heal, center)

        elif final_gesture == "OPEN":
            spells.cast_fireball(annotated, gif_fire, center)



    # Exibe o frame já processado (com efeitos e debug)
    cv2.imshow("D&D AR Spells", annotated)

    # ESC encerra o programa
    if cv2.waitKey(1) & 0xFF == 27:
        break



# ===================================================================
#  FINALIZAÇÃO
# ===================================================================

cap.release()                                    # Libera câmera
cv2.destroyAllWindows()                          # Fecha janelas
print("\nEncerrado.")
