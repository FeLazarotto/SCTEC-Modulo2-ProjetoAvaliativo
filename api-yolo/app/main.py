
from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from app.detector import detectar_objetos


app = FastAPI(
    title="API de Detecção de Objetos com YOLO",
    description="API que recebe imagens e detecta objetos usando YOLO.",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "mensagem": "API YOLO funcionando!",
        "documentacao": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect")
async def detectar(
    arquivo: UploadFile = File(...)
):
    # Aceita apenas formatos de imagem esperados.
    tipos_permitidos = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if arquivo.content_type not in tipos_permitidos:
        raise HTTPException(
            status_code=415,
            detail="Envie uma imagem JPEG, PNG ou WEBP."
        )

    # Limite inicial de 10 MB por arquivo.
    conteudo = await arquivo.read(10 * 1024 * 1024 + 1)

    if len(conteudo) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="A imagem deve ter no máximo 10 MB."
        )

    # Verifica se o conteúdo realmente é uma imagem.
    try:
        with Image.open(BytesIO(conteudo)) as imagem:
            imagem.verify()

    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="O arquivo enviado não é uma imagem válida."
        )

    # Executa a detecção.
    try:
        resultado = detectar_objetos(conteudo)

    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Não foi possível processar a imagem."
        )

    return {
        "arquivo": arquivo.filename,
        **resultado
    }
