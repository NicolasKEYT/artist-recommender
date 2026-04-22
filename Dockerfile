FROM python:3.11-slim

WORKDIR /app

# Instala dependências primeiro (cache de layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Variável de ambiente para o Python encontrar o pacote src
ENV PYTHONPATH=/app

CMD ["python", "scripts/run_pipeline.py"]
