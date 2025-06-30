FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y \
        pkg-config \
        default-libmysqlclient-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /api

COPY requerimientos.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requerimientos.txt

COPY . .

# Cambia el directorio de trabajo a donde está manage.py
WORKDIR /api/test_api

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]