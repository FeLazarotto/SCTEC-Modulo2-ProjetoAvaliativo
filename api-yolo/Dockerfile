FROM python:3.11-slim

# Evita arquivos .pyc e mantém os logs visíveis.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Bibliotecas de sistema necessárias para algumas
# dependências de visão computacional.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências da aplicação.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código para a imagem.
COPY app/ ./app/

# Expõe a porta usada pelo servidor.
EXPOSE 8000

# Inicia a API.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]