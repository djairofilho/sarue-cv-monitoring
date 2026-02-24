# Saruê Detection (Camera Trap)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-0066FF?style=flat-square&logo=ultralytics&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Config](https://img.shields.io/badge/Config-PyYAML-grey?style=flat-square)

Sistema de detecção automática de saruês (gambás) em vídeos de câmera trap utilizando Deep Learning com YOLOv8.

## Objetivo do Projeto

Este projeto foi desenvolvido para automatizar a triagem de vídeos de câmeras trap, identificando frames que contenham saruês, anotando a localização do animal e extraindo os dados para análises futuras como contagem, comportamento e períodos de atividade.

## Escolhas Técnicas e Justificativas

- **YOLOv8 (Ultralytics)**: Foi selecionado por ser o padrão atual da indústria para detecção de objetos em tempo real. Sua arquitetura permite alta precisão mesmo em modelos pequenos (Nano), o que é ideal para processar grandes volumes de vídeos de pesquisa em hardware comum.
- **OpenCV**: Utilizado para a manipulação eficiente de arquivos de vídeo .AVI e renderização das anotações gráficas. É a biblioteca mais robusta para operações de baixo nível em frames.
- **Arquitetura Modular**: O código foi dividido em responsabilidades claras (Detector, Processor e Utils). Isso permite que, no futuro, o modelo de IA seja trocado ou a lógica de salvamento de arquivos seja alterada sem impactar o restante do sistema.
- **Configuração via YAML**: Centralizar hiperparâmetros em um arquivo externo facilita a experimentação por pesquisadores que não necessariamente desejam alterar o código Python.

## Estrutura do Projeto

```text
sarue-detection/
│
├── data/               # Diretório para vídeos de entrada (.AVI)
├── outputs/            # Resultados gerados automaticamente
│   ├── frames_raw/         # Frames originais com detecção confirmada
│   ├── frames_annotated/   # Frames com bounding boxes desenhadas
│   ├── video_annotated/    # Vídeo final com as detecções renderizadas
│   └── detections.csv      # Log detalhado (coordenadas, confiança e tempo)
│
├── src/                # Código fonte
│   ├── detector.py         # Lógica de inferência e desenho do modelo
│   ├── video_processor.py  # Orquestração do pipeline de vídeo
│   ├── utils.py            # Gerenciamento de arquivos e escrita de dados
│   └── main.py             # Interface de linha de comando (CLI)
│
├── requirements.txt    # Lista de dependências do projeto
├── config.yaml         # Todas as configurações de modelo e saídas
└── README.md
```

## Instalação

1. Certifique-se de ter o Python 3.10 ou superior instalado.
2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Como utilizar

Para processar um vídeo individual:

```bash
python src/main.py --video data/seu_video.avi --conf 0.4
```

Para processar um diretório completo de vídeos:

```bash
python src/main.py --video data/
```

### Argumentos CLI

- `--video`: Caminho obrigatório para o arquivo de vídeo ou diretório contendo vídeos.
- `--conf`: (Opcional) Define o nível mínimo de confiança para considerar uma detecção válida (0.0 a 1.0). Sobrescreve o valor do arquivo de configuração.
- `--config`: (Opcional) Permite apontar para um arquivo YAML de configuração alternativo.

## Configuração (config.yaml)

O sistema é altamente customizável através do arquivo `config.yaml`:

- `weights`: Define qual arquivo de pesos carregar (ex: nano, small, medium).
- `target_class_id`: Filtro de classe (ex: 16 para 'cat'). Deve ser definido como `null` para detectar todas as classes ou quando usar um modelo treinado especificamente.
- `save_csv`: Habilita ou desabilita a geração do relatório de detecções.

## Próximos Passos

1. **Fine-Tuning Especializado**: Treinar o modelo com imagens reais do projeto de pesquisa para que ele aprenda a distinguir saruês de outros animais de porte similar com maior precisão.
2. **Algoritmos de Rastreamento (Tracking)**: Implementar rastreio de objetos para identificar indivíduos únicos cruzando a câmera, evitando que um mesmo animal seja contado múltiplas vezes.
3. **Melhoria de Imagem Noturna**: Implementar filtros de pré-processadores para aumentar o contraste em imagens de infravermelho, facilitando a detecção em condições críticas de luz.
4. **Análise de Metadados**: Implementar OCR (Reconhecimento Óptico de Caracteres) para ler a data e hora carimbadas na imagem pelos modelos de câmera trap, organizando os dados cronologicamente.

## Licença

Este projeto está sob a licença [MIT](LICENSE).
