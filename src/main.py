"""
main.py — Ponto de entrada CLI do sistema de detecção de Saruê.

Uso:
  python src/main.py --video data/video.avi --conf 0.4
"""

import argparse
import os
import sys

# Adiciona o diretório atual ao path para permitir imports modulares
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import load_config, init_csv
from src.detector import SarueDetector
from src.video_processor import process_video

def main():
    parser = argparse.ArgumentParser(description="Detecção Automática de Saruês em Vídeos de Câmera Trap")
    
    parser.add_argument("--video", type=str, required=True, help="Caminho para o arquivo de vídeo .avi ou diretório")
    parser.add_argument("--conf", type=float, help="Threshold de confiança (opcional, sobrescreve config)")
    parser.add_argument("--config", type=str, default="config.yaml", help="Caminho para o arquivo de config")
    
    args = parser.parse_args()

    # 1. Carrega Configurações
    if not os.path.exists(args.config):
        print(f"Erro: Arquivo de configuração '{args.config}' não encontrado.")
        return
    
    config = load_config(args.config)

    # Sobrescreve confiança se passado no CLI
    if args.conf:
        config['detection']['confidence'] = args.conf

    # 2. Inicializa Detector
    print("Inicializando modelo YOLOv8...")
    detector = SarueDetector(
        model_path=config['model']['weights'],
        conf_threshold=config['detection']['confidence'],
        target_class_id=config['model']['target_class_id']
    )

    # 3. Inicializa CSV de saída
    csv_path = os.path.join("outputs", "detections.csv")
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    init_csv(csv_path)

    # 4. Processa Vídeo(s)
    target = args.video
    if os.path.isdir(target):
        videos = [os.path.join(target, f) for f in os.listdir(target) if f.lower().endswith('.avi')]
        if not videos:
            print(f"Nenhum vídeo .avi encontrado em {target}")
            return
        
        print(f"Foram encontrados {len(videos)} vídeos para processar.")
        for v in videos:
            process_video(v, detector, config)
    else:
        if os.path.exists(target):
            process_video(target, detector, config)
        else:
            print(f"Erro: Arquivo ou diretório '{target}' não encontrado.")

if __name__ == "__main__":
    main()
