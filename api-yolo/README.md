# API de Detecção de Objetos com YOLO

API construída com FastAPI que recebe imagens e usa o modelo YOLO11n para detectar objetos. São aceitas imagens JPEG, PNG e WEBP de até 10 MB.

## Requisitos

- Python 3.11 ou superior
- Docker e Docker Compose (para executar em contêiner)

Na primeira inicialização, o Ultralytics baixa o arquivo de pesos `yolo11n.pt`. É necessário ter acesso à internet para esse download.

## Executar com Docker Compose

No terminal, entre na pasta `api-yolo` e inicie a aplicação:

```powershell
cd api-yolo
docker compose up --build
```

A API ficará disponível em `http://localhost:8000`. Para parar os contêineres, pressione `Ctrl+C`; para executar em segundo plano, use `docker compose up --build -d` e encerre com `docker compose down`.

## Executar localmente

Na pasta `api-yolo`, crie e ative um ambiente virtual e instale as dependências:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Inicie o servidor:

```powershell
uvicorn app.main:app --reload
```

## Endpoints

| Método | Caminho | Descrição |
|---|---|---|
| `GET` | `/` | Verifica se a API está disponível e informa o caminho da documentação. |
| `GET` | `/health` | Retorna o estado de saúde da API. |
| `POST` | `/detect` | Recebe uma imagem e retorna os objetos detectados. |

A documentação interativa do FastAPI está disponível em `http://localhost:8000/docs`.

## Classes detectadas

O modelo pré-treinado `yolo11n.pt` detecta 80 classes do conjunto COCO. Os nomes das classes são retornados em inglês pela API:

- **Pessoas e transporte:** `person`, `bicycle`, `car`, `motorcycle`, `airplane`, `bus`, `train`, `truck`, `boat`.
- **Sinalização e ambiente urbano:** `traffic light`, `fire hydrant`, `stop sign`, `parking meter`, `bench`.
- **Animais:** `bird`, `cat`, `dog`, `horse`, `sheep`, `cow`, `elephant`, `bear`, `zebra`, `giraffe`.
- **Acessórios e bagagem:** `backpack`, `umbrella`, `handbag`, `tie`, `suitcase`.
- **Esportes:** `frisbee`, `skis`, `snowboard`, `sports ball`, `kite`, `baseball bat`, `baseball glove`, `skateboard`, `surfboard`, `tennis racket`.
- **Utensílios e alimentos:** `bottle`, `wine glass`, `cup`, `fork`, `knife`, `spoon`, `bowl`, `banana`, `apple`, `sandwich`, `orange`, `broccoli`, `carrot`, `hot dog`, `pizza`, `donut`, `cake`.
- **Móveis e itens domésticos:** `chair`, `couch`, `potted plant`, `bed`, `dining table`, `toilet`.
- **Eletrônicos e objetos diversos:** `tv`, `laptop`, `mouse`, `remote`, `keyboard`, `cell phone`, `microwave`, `oven`, `toaster`, `sink`, `refrigerator`, `book`, `clock`, `vase`, `scissors`, `teddy bear`, `hair drier`, `toothbrush`.

### Detectar objetos

Envie uma requisição `multipart/form-data` para `/detect`, usando `arquivo` como nome do campo:

```powershell
curl.exe -X POST "http://localhost:8000/detect" -F "arquivo=@imagem.jpg"
```

A resposta inclui o nome do arquivo, a quantidade de objetos detectados e, para cada objeto, sua classe, confiança e coordenadas da caixa delimitadora:

```json
{
  "arquivo": "imagem.jpg",
  "quantidade": 1,
  "deteccoes": [
    {
      "classe": "person",
      "confianca": 0.9231,
      "caixa": {
        "x1": 120.5,
        "y1": 45.2,
        "x2": 310.8,
        "y2": 480.1
      }
    }
  ]
}
```

Erros comuns do endpoint `/detect`:

- `400`: o conteúdo enviado não é uma imagem válida.
- `413`: a imagem excede o limite de 10 MB.
- `415`: o tipo informado não é JPEG, PNG ou WEBP.
- `422`: arquivo obrigatório ausente ou falha ao processar a imagem.

## Testes

Com as dependências instaladas, execute na pasta `api-yolo`:

```powershell
pytest
```