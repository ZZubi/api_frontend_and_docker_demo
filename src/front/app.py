import streamlit as st
import requests
import configparser

# 1. Configuración de la página
st.set_page_config(page_title="Experto en Bricolaje 🪚", page_icon="🛠️", layout="wide")
st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            <style>
            /* Estilo para el texto de las pestañas */
            button[data-baseweb="tab"] p {
                font-size: 24px;         /* Tamaño de la fuente */
                font-weight: bold;      /* Grosor de la fuente */
            }

            /* Estilo para aumentar el espacio (padding) de la pestaña */
            button[data-baseweb="tab"] {
                height: 60px;           /* Altura de la pestaña */
                width: 100%;            /* Opcional: ajustar ancho */
            }
            </style>
            """
st.markdown(st_style, unsafe_allow_html=True) # Esconde los elementos específicos de streamlit

# 2. Carga de configuración desde config.ini
config = configparser.ConfigParser()
config.read('./config.ini')

try:
    host = config.get('frontend','api_host')
    port = config.get('frontend','api_port')
    endpoint_url = f"http://{host}:{port}/ask_a_question"
except KeyError:
    st.error("Error: No se encontró la configuración de la API en config.ini")
    st.stop()

# 3. Interfaz de Usuario (Frontend)
st.title("🛠️ Consulta a tu experto en bricolaje del hogar 🧑‍🔧")

# Formulario:
with st.form(key="my_form", clear_on_submit=False):
    # Área de texto para la pregunta
    user_question = st.text_area("Introduce tu pregunta aquí:", placeholder="Ej: ¿Cómo arreglar una cisterna que gotea?")

    # El botón de formulario es especial: se llama 'form_submit_button'
    submit_button = st.form_submit_button(label="Enviar pregunta")

# Botón de envío
if submit_button:
    # Validación: ¿Está el área de texto vacía?
    if not user_question.strip():
        st.warning("Antes tienes que escribir una pregunta")
    else:
        # Preparación de la petición
        payload = {"question": user_question}
        
        try:
            with st.spinner("Consultando al experto..."):
                response = requests.post(endpoint_url, json=payload)
                data = response.json()

            # Gestión de la respuesta según los requisitos
            if data.get('error') == False:
                st.subheader("Respuesta del experto:")
                st.write(data.get('answer'))
            
            else:
                st.error(f"Ha ocurrido un error:\n{data.get('error_msg')}")
                
        except requests.exceptions.ConnectionError as ex:
            st.error("No se pudo conectar con el servidor. Asegúrate de que la API esté corriendo.")
        except Exception as e:
            st.error(f"Error inesperado: {e}")

# Pie de página opcional
st.markdown("---")
st.caption("Herramienta de ayuda para reformas y mantenimiento del hogar.")