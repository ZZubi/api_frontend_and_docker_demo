import requests
from api import functions as f

def test_success_on_ask_a_question():
    _, api_port, _ = f.get_api_config()
    url = f"http://127.0.0.1:{api_port}/ask_a_question"  

    data = {'question': 'cuéntame un chiste corto'}
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["answer"], str)
    assert len(response_json["answer"]) > 0
    assert response_json["error"] == False

def test_error_01_on_ask_a_question():
    api_host, api_port, _ = f.get_api_config()
    url = f"http://127.0.0.1:{api_port}/ask_a_question"  

    data = {'not_valid_json_key': 'whatever_content'}
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json["error"] == True
    assert response_json["error_msg"] == "Invalid JSON format"

def test_error_02_on_ask_a_question():
    api_host, api_port, _ = f.get_api_config()
    url = f"http://127.0.0.1:{api_port}/ask_a_question"  

    data = {'question': ''} # Empty question
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json["error"] == True
    assert response_json["error_msg"] == "Invalid JSON format"

def test_error_03_on_ask_a_question():
    api_host, api_port, _ = f.get_api_config()
    url = f"http://127.0.0.1:{api_port}/ask_a_question"  

    response = requests.post(url, json=None) # No data sent on the request
    response_json = response.json()
    assert response.status_code == 400
    assert response_json["error"] == True
    assert response_json["error_msg"] == "Invalid JSON format"