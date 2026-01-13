docker build -t arrizeta/api_project:0.0.2 . # on same folder where dockerfile is
docker images # lists images, check if it was creted
docker run -p 8000:8000 -p 8501:8501 --name mi-contenedor-<version> <IMAGE_ID>
Ejemplo: docker run -p 8000:8000 -p 8501:8501 --name mi-contenedor-0.0.6 6b856c6041ac