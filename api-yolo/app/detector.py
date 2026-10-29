
from io import BytesIO
from PIL import Image
from ultralytics import YOLO


# Carrega o modelo pré-treinado.
# Na primeira execução, o arquivo dos pesos
# será baixado se ainda não estiver disponível.
modelo = YOLO("yolo11n.pt")


def detectar_objetos(conteudo: bytes) -> dict:
    """
    Recebe os bytes de uma imagem e retorna
    os objetos detectados em formato de dicionário.
    """

    # Abre a imagem recebida e converte para RGB.
    imagem = Image.open(BytesIO(conteudo)).convert("RGB")

    # Executa a detecção.
    resultados = modelo.predict(
        source=imagem,
        conf=0.25,
        verbose=False
    )

    resultado = resultados[0]
    deteccoes = []

    # Percorre cada objeto encontrado.
    if resultado.boxes is not None:
        for caixa in resultado.boxes:
            classe_id = int(caixa.cls.item())
            confianca = float(caixa.conf.item())
            coordenadas = caixa.xyxy[0].tolist()

            deteccoes.append({
                "classe": resultado.names[classe_id],
                "confianca": round(confianca, 4),
                "caixa": {
                    "x1": round(coordenadas[0], 2),
                    "y1": round(coordenadas[1], 2),
                    "x2": round(coordenadas[2], 2),
                    "y2": round(coordenadas[3], 2)
                }
            })

    return {
        "quantidade": len(deteccoes),
        "deteccoes": deteccoes
    }
