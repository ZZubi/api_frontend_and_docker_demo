import configparser
import psycopg2
from datetime import datetime, timezone
from groq import Groq

def get_api_config():
    # 1. Crear la instancia del objeto config
    config = configparser.ConfigParser()

    # 2. Leer archivo de config
    config.read('./config.ini')

    # 3. Acceder a los datos como si fuera un diccionario
    host = config.get('api', 'host')
    port = config.getint('api', 'port')  # .getint lo convierte automáticamente a entero
    is_debug = config.getboolean('api', 'debug') # .getboolean maneja 'True'/'False'

    return host, port, is_debug

def get_db_config():
    # 1. Crear la instancia del objeto config
    config = configparser.ConfigParser()

    # 2. Leer archivo de config
    config.read('./config.ini')

    # 3. Acceder a los datos como si fuera un diccionario
    user = config.get('database', 'user')
    password = config.get('database', 'password')
    host = config.get('database', 'host')
    port = config.get('database', 'port')
    db_name = config.get('database', 'db_name')

    return user, password, host, port, db_name

def get_aiservice_config():
    # 1. Crear la instancia del objeto config
    config = configparser.ConfigParser()

    # 2. Leer archivo de config
    config.read('./config.ini')

    # 3. Acceder a los datos como si fuera un diccionario
    api_key = config.get('ai_service', 'free_api_key')

    return api_key

def make_question_to_ai_model(question: str):
    try:
        api_key = get_aiservice_config()
        client = Groq(
            api_key=api_key)
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
            {
                "role": "user",
                "content": f"{question}"
            }
            ],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None
        )

        answer = ""
        for chunk in completion:
            answer += chunk.choices[0].delta.content or ""

        #print(answer)
        return answer

    except Exception as e:
        raise Exception(f"Error al consultar al agente de IA: {e}")
    

    

def save_ai_query_to_db(question: str, answer: str):
    connection = None
    error = False
    user, password, host, port, db_name = get_db_config()

    try:
        # 1. Configurar la conexión
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=db_name
        )
        cursor = connection.cursor()

        # 2. Definir la sentencia SQL con placeholders (%s) para evitar SQL Injection
        insert_query = """
            INSERT INTO ai_query_log (question, answer, utc_datetime) 
            VALUES (%s, %s, %s)
        """
        
        # 3. Preparar los datos (usando el tiempo actual en UTC)
        record_to_insert = (question, answer, datetime.now(timezone.utc))

        # 4. Ejecutar y confirmar
        cursor.execute(insert_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as e:
        error = f"Error al guardar en BBDD: {e}"
        if connection:
            connection.rollback()

    finally:
        # 5. Cerrar la conexión
        if connection:
            cursor.close()
            connection.close()


    if error != False:
        raise Exception(f"Error al guardar en BBDD: {error}") # Manejaremos el error en la llamada a la API