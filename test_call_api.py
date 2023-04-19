import requests

ENDPOINT = 'http://127.0.0.1:8000/consulta-sii{0}'

errores = {
    'tipo_fecha': 'El formato de fecha no coincide. Intente nuevamente con el formato DD-MM-YYYY',
    'fecha_minima': 'La fecha mínima permitida es el 01-01-2013',
    'anio_futuro': 'El anio no puede ser mayor al anio actual',
    'campo_obligatorio': 'La fecha es un campo obligatorio.'
}

def test_can_call_endpoint():
    fecha = '?fecha=01-01-2013'
    response = requests.get(ENDPOINT.format(fecha))

    assert response.status_code == 200

def test_check_response_values():
    fecha = '?fecha=01-01-2013'
    response = requests.get(ENDPOINT.format(fecha))
    json_data = response.json()

    assert ('fecha_ingresada' and 'valor_unidad_fomento' in json_data)\
        and (json_data['fecha_ingresada'] == '01-01-2013' and json_data['valor_unidad_fomento'] == '22.837,06')

def test_check_error_datatype():
    fecha = '?fecha=x'
    response = requests.get(ENDPOINT.format(fecha))
    json_data = response.json()

    assert 'error' in json_data and json_data['error'] == errores['tipo_fecha']

def test_check_missing_param():
    response = requests.get(ENDPOINT.format(''))
    json_data = response.json()

    assert 'error' in json_data and json_data['error'] == errores['campo_obligatorio']