FROM python:3.12-slim

# Directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias primero
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear directorio para la base de datos SQLite
RUN mkdir -p /app/data

# Exponer el puerto
EXPOSE 8001

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
