# Usa una imagen base ligera de Python 3.11
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias
COPY requirements.txt .

# Instala dependencias del sistema necesarias para pandas y SQLite
RUN pip install --no-cache-dir -r requirements.txt
# Copia el resto de la aplicación
COPY . .

# Dar permisos de ejecución al script de inicio
WORKDIR /app/src
RUN chmod +x run_all.sh

# Expone el puerto de Flask (por defecto 5000)
EXPOSE 8000

# Expone el puerto de streamlit (por defecto 8501)
EXPOSE 8501

# Ejecutar el script que levanta la API y el frontend de Streamlit:
CMD ["./run_all.sh"]
