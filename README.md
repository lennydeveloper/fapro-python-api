# fapro-python-api
El Servicio de Impuestos Internos (SII) de Chile mantiene una tabla con los valores de la Unidad de Fomento actualizados para cada año. Tu desafío consiste en crear una API en Python que permita a los usuarios consultar el valor de la Unidad de Fomento para una fecha específica.

![Valores de la Unidad de Fomento](https://user-images.githubusercontent.com/3030497/232532665-86703af1-3e7e-4147-9fe1-89cd35889334.png)

### Requisitos

- Python 3.7+

### Requisitos predefinidos del API:

- La API debe estar desarrollada en Python utilizando la librería "requests" u otra similar.
- No se puede utilizar Selenium debido al alto consumo de recursos que estas herramientas implican.
- La API debe permitir consultar el valor de la Unidad de Fomento para una fecha específica, la cual debe ser ingresada como parámetro en la solicitud.
- La fecha mínima que se puede consultar es el 01-01-2013, y no hay fecha máxima, ya que la tabla se actualiza constantemente.
- La API debe devolver el valor de la Unidad de Fomento correspondiente a la fecha consultada.
- La respuesta de la API debe estar en formato JSON.

### Instalación (local)

- Python 3.7+ requerido

```bash
pip install -r requirements.txt
uvicorn main:app
```

### Despliegue

El sitio (backend) se encuentra desplegado en el siguiente [enlace](https://fapro-python-api.onrender.com)

### Endpoints

- 127.0.0.1:8000/consulta-sii

### Parámetros

- fecha: El sistema requiere una fecha ya que el objetivo de este es retornar un valor de fomento para una fecha específica. Por ejemplo: [localhost:8000/consulta-sii?fecha=01-01-2013](http://127.0.0.1:8000/consulta-sii?fecha=01-01-2013)

PD: formato de fecha permitido por el sistema: DD-MM-YYYY (validación directa al tipo de dato dado por el valor "fecha")


# Testing

```bash
# activate your virtual environment first
pytest
```

Esto ejecutará automáticamente los tests dentro del archivo "test_call_api.py"
