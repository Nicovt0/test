FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y \
        pkg-config \
        default-libmysqlclient-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor (ajusta si es necesario)
WORKDIR /api

# Copia requerimientos y los instala primero (mejor para caché)
COPY requerimientos.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requerimientos.txt

# Copia el resto del código al contenedor
COPY . .

# Cambia el directorio de trabajo a donde está manage.py
# Si tu manage.py está en /app, no cambies el WORKDIR
# Si está en /app/testv, cambia el WORKDIR a /app/testv
WORKDIR /api/test

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]