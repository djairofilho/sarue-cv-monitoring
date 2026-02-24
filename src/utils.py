"""
utils.py — Funções auxiliares reutilizáveis para o projeto Saruê Detection.

Responsabilidades:
  - Criação de diretórios de saída
  - Leitura de configuração YAML
  - Inicialização e escrita do arquivo CSV de detecções
"""

import csv
import os
from pathlib import Path
from typing import List

import yaml


# ---------------------------------------------------------------------------
# Diretórios
# ---------------------------------------------------------------------------

def ensure_output_dirs(base_output: str) -> dict:
    """
    Garante que os diretórios de saída existam, criando-os se necessário.

    Args:
        base_output: Caminho base da pasta outputs/.

    Returns:
        Dicionário com os caminhos de cada subpasta.
    """
    dirs = {
        "frames_raw":       os.path.join(base_output, "frames_raw"),
        "frames_annotated": os.path.join(base_output, "frames_annotated"),
        "video_annotated":  os.path.join(base_output, "video_annotated"),
    }
    for path in dirs.values():
        Path(path).mkdir(parents=True, exist_ok=True)
    return dirs


# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

def load_config(config_path: str) -> dict:
    """
    Carrega o arquivo de configuração YAML.

    Args:
        config_path: Caminho para config.yaml.

    Returns:
        Dicionário com as configurações.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# CSV de detecções
# ---------------------------------------------------------------------------

CSV_HEADER = ["video_file", "frame_id", "x1", "y1", "x2", "y2", "confidence", "class_name"]


def init_csv(csv_path: str) -> None:
    """
    Cria (ou sobrescreve) o arquivo CSV com o cabeçalho padrão.

    Args:
        csv_path: Caminho completo para o arquivo .csv.
    """
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)


def append_detections_to_csv(
    csv_path: str,
    video_name: str,
    frame_id: int,
    detections: List[dict],
) -> None:
    """
    Registra as detecções de um frame no arquivo CSV.

    Args:
        csv_path:   Caminho para o arquivo CSV.
        video_name: Nome do arquivo de vídeo processado.
        frame_id:   Número do frame atual.
        detections: Lista de detecções, cada uma com keys:
                    x1, y1, x2, y2, confidence, class_name.
    """
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for det in detections:
            writer.writerow([
                video_name,
                frame_id,
                det["x1"],
                det["y1"],
                det["x2"],
                det["y2"],
                f"{det['confidence']:.4f}",
                det["class_name"],
            ])
