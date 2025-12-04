from ultralytics import YOLO   # Importa a classe principal da família YOLOv8 (Ultralytics)


class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt"):
        # --------------------------------------------------------------
        # Carrega o modelo YOLO especificado.
        #
        # model_path pode ser:
        #   - um arquivo local (.pt)
        #   - o nome de um modelo pré-treinado disponível no hub:
        #       "yolov8n.pt"  = nano (rápido, leve)
        #       "yolov8s.pt"  = small
        #       "yolov8m.pt"  = medium
        #       "yolov8l.pt"  = large
        #       "yolov8x.pt"  = extra large
        #
        # Quando você chama YOLO(model_path):
        #   • carrega a arquitetura e pesos
        #   • inicializa pré-processamento interno (resize, normalize)
        #   • prepara a inferência em PyTorch
        #
        # O YOLOv8 usa um pipeline automático de:
        #   - conversão de imagem p/ tensor
        #   - normalização
        #   - pad + resize mantendo aspecto
        #   - inferência
        #   - decodificação de bounding boxes
        #   - NMS (Non-Max Suppression)
        # --------------------------------------------------------------
        self.model = YOLO(model_path)



    def detect(self, frame):
        # --------------------------------------------------------------
        # Executa a detecção no frame recebido do OpenCV (BGR).
        #
        # YOLO aceita BGR ou RGB automaticamente — ele converte
        # internamente para o formato apropriado antes da inferência.
        #
        # Parâmetros:
        #   frame : np.ndarray (imagem BGR original da câmera)
        #
        #   conf=0.5 :
        #       Confiança mínima para considerar uma detecção válida.
        #       Ex: se a probabilidade for < 0.5, a caixa é ignorada.
        #
        # Retorno:
        #   results : lista de objetos ultralytics.yolo.engine.results.Results
        #
        # Cada "Results" contém:
        #   .boxes → bounding boxes + scores + classes
        #   .masks → (se modelo for segmentação)
        #   .probs → (se modelo for classificação)
        #   .orig_img → frame original usado
        #   .plot()  → retorna imagem anotada com caixas e labels
        #
        # results é sempre uma lista, mesmo que só exista 1 imagem.
        # --------------------------------------------------------------
        results = self.model(frame, conf=0.5)



        # --------------------------------------------------------------
        # results[0] = primeiro resultado da lista (única imagem)
        #
        # Por quê?
        #   O YOLO sempre retorna uma lista — porque você pode enviar
        #   várias imagens ao mesmo tempo.
        #
        # Como você usa apenas um frame por vez, basta pegar o índice 0.
        # --------------------------------------------------------------
        return results[0]   # retorna a estrutura completa de resultados
