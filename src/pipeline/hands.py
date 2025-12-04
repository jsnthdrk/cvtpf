import mediapipe as mp   # Importa a MediaPipe, que contém o modelo de detecção e tracking de mãos
import cv2               # OpenCV, usado para converter BGR→RGB e manipular o frame


class HandTracker:
    def __init__(self):
        # --------------------------------------------------------------
        # Criação da instância do modelo MediaPipe Hands
        # --------------------------------------------------------------
        #
        # A classe mp.solutions.hands.Hands configura:
        #
        # 1) Palm Detection Model:
        #       - Detecta uma mão nova no frame.
        #       - Funciona frame a frame.
        #
        # 2) Hand Landmark Model:
        #       - Extrai 21 pontos 3D da mão (landmarks).
        #       - Faz tracking entre frames (se já detectou antes).
        #
        # Esses dois modelos rodam em pipeline, e a MediaPipe decide
        # automaticamente quando cada um será usado.
        #
        self.hands = mp.solutions.hands.Hands(
            model_complexity=1,          # Qualidade do modelo: 0 → mais leve, 1 → equilibrado, 2 → mais preciso
            max_num_hands=2,             # Limita deteção para até 2 mãos simultâneas
            min_detection_confidence=0.7,# Confiança mínima para detectar uma nova mão no frame
            min_tracking_confidence=0.6  # Confiança mínima para continuar rastreando uma mão já detectada
        )

        # --------------------------------------------------------------
        # drawing_utils:
        # Ferramentas internas da MediaPipe para desenhar landmarks
        # e conexões (ossos) diretamente na imagem.
        # --------------------------------------------------------------
        self.drawer = mp.solutions.drawing_utils

        # --------------------------------------------------------------
        # HAND_CONNECTIONS:
        # Lista de arestas que conectam os 21 landmarks formando
        # a estrutura óssea da mão.
        #
        # Ex: (0,5) liga o pulso ao início do dedo indicador.
        # --------------------------------------------------------------
        self.connections = mp.solutions.hands.HAND_CONNECTIONS



    def process(self, frame):
        # --------------------------------------------------------------
        # MediaPipe exige entrada em RGB.
        #
        # OpenCV utiliza BGR por padrão, então é necessário inverter
        # a ordem dos canais para que o modelo interprete corretamente.
        #
        # Se você não fizer essa conversão:
        #    - a detecção falha ou
        #    - os landmarks vêm totalmente distorcidos.
        # --------------------------------------------------------------
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # --------------------------------------------------------------
        # Executa a inferência do modelo de mãos no frame RGB.
        #
        # Retorno (objeto `HandsResult`):
        #
        # results.multi_hand_landmarks:
        #       - Lista de mãos detectadas.
        #       - Cada mão contém 21 landmarks com (x,y,z) normalizado.
        #
        # results.multi_hand_world_landmarks:
        #       - Versão em coordenadas reais (metros)
        #         usando o cálculo 3D interno da MediaPipe.
        #
        # results.multi_handedness:
        #       - Informação “Left” / “Right” estimada pelo modelo.
        #
        # O processamento envolve o pipeline inteiro da MediaPipe,
        # incluindo smoothing temporal e rastreamento de movimento.
        # --------------------------------------------------------------
        return self.hands.process(rgb)
