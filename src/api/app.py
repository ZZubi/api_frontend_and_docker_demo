from flask import Flask, request, jsonify
import functions as f

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def home():
    return "API desarrollada con Flask"

@app.route('/ask_a_question', methods=['POST'])
def ask_a_question():
    try:
        incoming_data = request.get_json()
        if not incoming_data or 'question' not in incoming_data or len(incoming_data['question']) == 0:
            raise Exception("Invalid JSON")
    except:
        return jsonify(
            {
                'error': True,
                'error_msg': 'Invalid JSON format'
            }), 400
        
    question = incoming_data['question']

    # Consultar a la IA y almacenar pregunta/respuesta en la BBDD:
    try:
        answer = f.make_question_to_ai_model(question)
        f.save_ai_query_to_db(question, answer)
    except Exception as e:
        return jsonify({
            'error': True,
            'error_msg': f"{e}"
            }), 400
    
    return jsonify({
        'answer': answer,
        'error': False
        }), 200

if __name__ == '__main__':
    host, api_port, is_debug = f.get_api_config()

    app.run(host=host, port=api_port, debug=is_debug)