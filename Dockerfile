# ---- Base ----
FROM python:3.11-slim


# Dependencias mínimas del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Instalar dependencias primero (mejor caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Puerto de la API
EXPOSE 5000

# Arranque con Gunicorn (2 workers es suficiente para demo)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
