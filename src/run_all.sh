#!/bin/bash

# Levantar la API de Flask en segundo plano (&)
python ./api/app.py &

# Esperar unos segundos para que la API esté lista
sleep 5

# Levantar Streamlit
streamlit run ./front/app.py --server.port=8501 --server.address=0.0.0.0