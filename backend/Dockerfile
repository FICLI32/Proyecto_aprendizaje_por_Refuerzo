# imagen de Python
FROM python:3.12-slim

# directorio de trabajo dentro del contenedor 
WORKDIR /app

# instala las dependencias del backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia el contenido del proyecto al contenedor
COPY . .

# expone el puerto 8000
EXPOSE 8000

# comando para iniciar FastAPI, permitiendo conexiones externas (0.0.0.0)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]