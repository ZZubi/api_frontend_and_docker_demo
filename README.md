# Agente de Bricolaje 🛠️

DEMO para aprender cómo empaquetar una API y un frontend en una imagen Docker

Se trata de un asistente para mantenimiento del hogar que responde a dudas de bricolaje y tareas domésticas.  
La aplicación se compone de:

- **Frontend** desarrollado con **Streamlit**
- **API** desarrollada con **Flask**
- **Contenedor Docker** que empaqueta todo y expone la aplicación en el puerto `8501`

> ⚠️ **IMPORTANTE**  
> **Todos los comandos (instalación, ejecución, tests, etc.) deben ejecutarse siempre desde la carpeta `./src`.**  
> Por ejemplo, si clonas el repositorio en `~/proyectos/api_frontend_and_docker_demo`, primero navega a:
>
> ```bash
> cd ~/proyectos/api_frontend_and_docker_demo/src
> ```
>
> y desde ahí lanza el resto de comandos.

---

## 1. Requisitos previos

- [Python](https://www.python.org/) (recomendado 3.12)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Docker Desktop](https://docs.docker.com/get-docker/) (opcional, si queremos ejecutar vía contenedor)

---

## 2. Clonado del repositorio

```bash
git clone https://github.com/ZZubi/api_frontend_and_docker_demo.git
cd api_frontend_and_docker_demo
```

> Recuerda: a partir de aquí, **toda la ejecución se hace desde `./src`**:
>
> ```bash
> cd src
> ```

---

## 3. Configuración de secretos (`secrets.ini`)

Antes de arrancar la aplicación es necesario crear un fichero de configuración con los datos sensibles:

1. En la **raíz del proyecto** (donde está el propio `secrets.sample.ini`), crea un fichero llamado `secrets.ini`.
2. Copia el contenido de `secrets.sample.ini` y utilízalo como plantilla.
3. Rellena los valores "*******" con tus datos sensibles (tokens, claves, etc.):

```ini
# secrets.ini (ejemplo)
[api]
host = 0.0.0.0
port = 9000
debug = True

[frontend]
api_host = 127.0.0.1
api_port = 9000

[database]
user = *******
password = *******
host = dpg-d5if3rkhg0os738i40jg-a.frankfurt-postgres.render.com
port = 5432
db_name = *******

[ai_service]
free_api_key = *******
```

- El fichero `secrets.ini` **está ignorado en `.gitignore`** precisamente porque contiene información sensible y **no debe subirse al repositorio.**
- `secrets.sample.ini` sirve como **plantilla pública** sin valores reales.


---

## 4. Estructura básica del proyecto

A alto nivel, la estructura del repositorio es:

```text
api_frontend_and_docker_demo/
├─ src/
│  ├─ frontend/        # Código Streamlit (interfaz de usuario)
│  ├─ api/             # Código Flask (endpoints del agente)
│  ├─ test_api.txt     # Tests de la API desarrollada en Flask
│  ├─ requirements.txt # Dependencias de Python
│  └─ ...
├─ Dockerfile          # Imagen Docker que empaqueta API + frontend
├─ secrets.sample.ini  # Plantilla de configuración de secretos
└─ .gitignore          # Incluye secrets.ini, entre otros
```

*(La estructura exacta puede variar ligeramente; consulta el árbol real del repo para más detalle.)*

---

## 5. Ejecución en local (sin Docker)

1. Asegúrate de tener creado y configurado `secrets.ini` en la raíz del proyecto.
2. Activa el entorno virtual e instala dependencias (ver sección anterior).
3. Desde `./src`, lanza la API :

```bash
python api/app.py
```

Por defecto, Flask expondrá la API en:

```text
http://localhost:9000
```

4. Desde `./src`, lanza el frontend de Streamlit:

```bash
cd src
streamlit run frontend/app.py
```

Por defecto, Streamlit expondrá la aplicación en:

```text
http://localhost:8501
```

---

## 6. Ejecución con Docker

La forma más sencilla de ejecutar todo el stack (API Flask + frontend Streamlit) es usando Docker.

Desde la **raíz del proyecto**:

```bash
# Construir la imagen
docker build -t api_project:0.1.0 .

# Ejecutar contenedor
docker run --rm -p 8501:8501 -p 9000:9000 --name api_project api_project:0.1.0
```

- El contenedor expondrá el puerto `9000` (Flask API) hacia tu máquina.
- El contenedor expondrá el puerto `8501` (Streamlit) hacia tu máquina.
- Accede a la aplicación en:

```text
http://localhost:8501
```

> Nota: Si necesitas pasar el fichero `secrets.ini` al contenedor, puedes:
>
> - Usar un volumen:
>   ```bash
>   docker run --rm -p 8501:8501 \
>     -v "$(pwd)/secrets.ini:/app/secrets.ini:ro" \
>     --name agente-bricolaje agente-bricolaje
>   ```
> - O construir la imagen incluyendo los secretos en el contexto de build (no recomendable para producción).

---

## 7. Ejecución de tests

> ⚠️ **Recuerda:** Todos los comandos de tests deben lanzarse **desde `./src`**.

Ejemplo (pytest):

```bash
cd src
pytest ./test.apy.py
```

---

## 8. Descripción funcional

El **Agente de Bricolaje** está orientado a ayudar al usuario en tareas como:

- Mantenimiento general del hogar
- Reparaciones básicas y bricolaje
- Sugerencias de herramientas y materiales
- Pasos detallados para acometer pequeñas obras o arreglos domésticos

El usuario interactúa mediante la interfaz de **Streamlit**, que envía sus preguntas a la **API Flask**.  
La API procesa la petición, utiliza la lógica del agente (por ejemplo, modelos de lenguaje o reglas definidas) y devuelve una respuesta estructurada que se muestra en el frontend.

---

## 9. Base de datos

La base de datos para esta demo tiene una sola tabla, que puede crearse mediante este SQL:

```sql
CREATE TABLE ai_query_log (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT,
    utc_datetime TIMESTAMP WITH TIME ZONE DEFAULT (now() AT TIME ZONE 'UTC')
);
```

---

## 10. Notas finales

- Nunca subas tu `secrets.ini` al repositorio remoto.
- Mantén tus claves y tokens fuera del repositorio.
- Verifica siempre que tus cambios no rompen los tests antes de abrir un PR.