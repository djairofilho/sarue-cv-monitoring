"""
detector.py — Wrapper para o modelo YOLOv8 da Ultralytics.

Responsabilidades:
  - Carregamento do modelo
  - Execução de inferência em frames individuais
  - Filtragem de resultados por confiança e classe
"""

from ultralytics import YOLO
import cv2
import numpy as np

class SarueDetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.35, target_class_id=None):
        """
        Inicializa o detector YOLOv8.

        Args:
            model_path: Caminho para o arquivo .pt (ex: yolov8n.pt).
            conf_threshold: Threshold de confiança mínimo.
            target_class_id: ID da classe específica a detectar (Ex: 15 para pássaros no COCO).
                            Se None, detecta todas as classes.
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.target_class_id = target_class_id

    def detect(self, frame):
        """
        Executa a detecção em um frame.

        Args:
            frame: Imagem (numpy array) em formato BGR.

        Returns:
            Lista de dicionários contendo as detecções formatadas.
        """
        # Executa inferência
        results = self.model.predict(
            source=frame, 
            conf=self.conf_threshold, 
            verbose=False
        )
        
        detections = []
        
        # Processa resultados
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                
                # Filtra pela classe alvo, se especificada
                if self.target_class_id is not None and cls_id != self.target_class_id:
                    continue
                
                # Coordenadas [x1, y1, x2, y2]
                coords = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                
                detections.append({
                    "x1": int(coords[0]),
                    "y1": int(coords[1]),
                    "x2": int(coords[2]),
                    "y2": int(coords[3]),
                    "confidence": conf,
                    "class_id": cls_id,
                    "class_name": self.model.names[cls_id]
                })
        
        return detections

    def draw_detections(self, frame, detections, color=(0, 255, 0), thickness=2, font_scale=0.6):
        """
        Desenha as bounding boxes no frame.
        """
        annotated_frame = frame.copy()
        for det in detections:
            x1, y1, x2, y2 = det["x1"], det["y1"], det["x2"], det["y2"]
            label = f"{det['class_name']} {det['confidence']:.2f}"
            
            # Desenha retângulo
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, thickness)
            
            # Desenha fundo do label
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1)
            cv2.rectangle(annotated_frame, (x1, y1 - 20), (x1 + w, y1), color, -1)
            
            # Escreve texto
            cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1)
            
        return annotated_frame
