# 🐾 Saruê Detection (Camera Trap)

Sistema de detecção automática de saruês (gambás) em vídeos de câmera trap utilizando Deep Learning com YOLOv8.

## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido para automatizar a triagem de vídeos de câmeras trap, identificando frames que contenham saruês, anotando a localização do animal e extraindo os dados para análises futuras (contagem, comportamento, etc.).

## 🚀 Abordagem Técnica

*   **Detecção**: Utilizamos o framework **Ultralytics YOLOv8**, conhecido por sua alta velocidade e precisão em detecção de objetos em tempo real.
*   **Pipeline**: O sistema lê o vídeo frame a frame, aplica a inferência do modelo e filtra os resultados com base em um threshold de confiança (ajustável).
*   **Armazenamento**: frames positivos são salvos tanto em formato bruto (raw) quanto anotado (com bounding boxes). As coordenadas e métricas são exportadas para um arquivo CSV.

## 📂 Estrutura do Projeto

```text
sarue-detection/
│
├── data/               # Coloque seus vídeos .AVI aqui
├── outputs/            # Resultados automáticos
│   ├── frames_raw/         # Frames onde houve detecção (limpos)
│   ├── frames_annotated/   # Frames com caixas delimitadoras
│   └── video_annotated/    # Vídeo exportado com detecções
│   └── detections.csv      # Log de coordenadas e confiança
│
├── src/                # Código fonte
│   ├── detector.py         # Wrapper do YOLOv8
│   ├── video_processor.py  # Pipeline de vídeo
│   ├── utils.py            # Helpers e manipulação de arquivos
│   └── main.py             # Entrada principal (CLI)
│
├── requirements.txt    # Dependências do Python
├── config.yaml         # Configurações de modelo e saída
└── README.md
```

## 🛠️ Instalação

1.  Certifique-se de ter o **Python 3.10+** instalado.
2.  Instale as dependências:

```bash
pip install -r requirements.txt
```

## 💻 Como Rodar

Para processar um vídeo específico:

```bash
python src/main.py --video data/seu_video.avi --conf 0.4
```

Para processar uma pasta cheia de vídeos:

```bash
python src/main.py --video data/
```

### Argumentos CLI

*   `--video`: Caminho para o vídeo ou pasta.
*   `--conf`: (Opcional) Threshold de confiança. Valores entre 0.0 e 1.0 (ex: 0.4). Sobrescreve o `config.yaml`.
*   `--config`: (Opcional) Caminho para um arquivo de configuração diferente.

## ⚙️ Configuração (`config.yaml`)

Você pode ajustar o comportamento do sistema editando o arquivo `config.yaml`:

*   `weights`: Caminho para o modelo `.pt`. Por padrão usa o `yolov8n.pt`.
*   `target_class_id`: Permite filtrar apenas uma classe do COCO (ex: 16 para gato) até que um modelo específico de saruê seja treinado. Se `null`, detecta tudo.
*   `save_raw_frames`: Define se salva o frame original ao encontrar uma detecção.

## 🔬 Melhorias Futuras

1.  **Fine-tuning**: Treinar o YOLOv8 com um dataset específico de fauna brasileira (Saruê, Mão-pelada, etc.) para maior precisão específica.
2.  **Object Tracking**: Implementar SORT ou DeepSORT para evitar contagens duplicadas do mesmo indivíduo cruzando a câmera.
3.  **Validação Genética/Morfométrica**: Integrar metadados de detecção com bancos de dados de pesquisa biológica.
4.  **Integração Web**: Criar um dashboard para visualizar as estatísticas das detecções.

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).

## 📝 Citação

Se este projeto for útil para sua pesquisa acadêmica, por favor, considere citar:

```text
Insper - Pesquisa: Deteção de Saruês em Câmeras Trap (2024).
Disponível em: [URL_DO_REPOSITORIO]
```

---
*Desenvolvido para pesquisa acadêmica e monitoramento de vida selvagem.*
