"""
video_processor.py — Pipeline de processamento de vídeos.

Responsabilidades:
  - Leitura de vídeo frame a frame
  - Coordenação entre Detector e Utils para salvar arquivos
  - Barra de progresso do processamento
"""

import os
import cv2
from tqdm import tqdm
from .utils import append_detections_to_csv, ensure_output_dirs

def process_video(video_path, detector, config):
    """
    Processa um vídeo AVI completo.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Erro: Não foi possível abrir o vídeo {video_path}")
        return

    # Info do vídeo
    video_name = os.path.basename(video_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Prepara diretórios
    output_dirs = ensure_output_dirs("outputs")
    csv_path = os.path.join("outputs", "detections.csv")

    # Configura VideoWriter (se habilitado)
    writer = None
    if config['output']['save_annotated_video']:
        video_out_path = os.path.join(output_dirs['video_annotated'], f"annotated_{video_name}")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(video_out_path, fourcc, fps, (width, height))

    print(f"Processando: {video_name} ({total_frames} frames)...")
    
    frame_id = 0
    with tqdm(total=total_frames) as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Executa detecção
            detections = detector.detect(frame)

            if len(detections) > 0:
                # 1. Salva no CSV
                if config['output']['save_csv']:
                    append_detections_to_csv(csv_path, video_name, frame_id, detections)

                # 2. Salva Frame Raw
                if config['output']['save_raw_frames']:
                    frame_path = os.path.join(output_dirs['frames_raw'], f"{video_name}_f{frame_id}.jpg")
                    cv2.imwrite(frame_path, frame)

                # 3. Desenha e salva Frame Anotado
                annotated_frame = detector.draw_detections(
                    frame, 
                    detections, 
                    color=tuple(config['output']['bbox_color']),
                    thickness=config['output']['bbox_thickness'],
                    font_scale=config['output']['font_scale']
                )

                if config['output']['save_annotated_frames']:
                    ann_path = os.path.join(output_dirs['frames_annotated'], f"ann_{video_name}_f{frame_id}.jpg")
                    cv2.imwrite(ann_path, annotated_frame)
                
                # Usa frame anotado para o vídeo de saída se houver detecção
                display_frame = annotated_frame
            else:
                display_frame = frame

            # Escreve no vídeo final
            if writer:
                writer.write(display_frame)

            frame_id += 1
            pbar.update(1)

    cap.release()
    if writer:
        writer.release()
    print(f"Concluído: {video_name}")
