import requests
from bs4 import BeautifulSoup as bs
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from datetime import datetime, date

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

errores = {
    'tipo_fecha': 'El formato de fecha no coincide. Intente nuevamente con el formato DD-MM-YYYY',
    'fecha_minima': 'La fecha mínima permitida es el 01-01-2013',
    'anio_futuro': 'El anio no puede ser mayor al anio actual',
    'campo_obligatorio': 'La fecha es un campo obligatorio.'
}


def format_sii_url(anio: int):
    '''
    Esta función recibe un anio como parámetro
    Retorna la URL del SII formateada con el anio dado
    '''

    SII_URL = 'https://www.sii.cl/valores_y_fechas/uf/uf{0}.htm'
    anio_actual = date.today().strftime('%Y')

    if anio < 2013: return None, {'error': errores['fecha_minima']}
    if anio > int(anio_actual): return None, {'error': errores['anio_futuro']}

    return SII_URL.format(anio), ''


def obtener_datos_sii(anio: int):
    '''
    Realiza la consulta al SII con el anio proporcionado
    Obtiene los valores de unidades de fomento para el anio dado
    '''

    try:
        URL, msg = format_sii_url(anio)
        if msg != '': return msg

        r = requests.get(URL.format(anio))
        soup = bs(r.text, 'html.parser')
        rows = soup.css.select('div.meses#mes_all > div > table > tbody > tr > td')

        contador = 1
        dias = []
        info_meses = []

        for item in rows:
            text = item.text
            info_meses.append('0,0') if text.isspace() else info_meses.append(text)

            if contador == 12:
                dias.append(info_meses)
                contador = 1
                info_meses = []
            else:
                contador += 1

        return dias
    except Exception:
        return None


def generar_unidades_fomento(fecha: str = None):
    '''
    Obtiene como parámetro una fecha y en base a esta obtiene todos los valores
    de unidades de fomento del presente año para la fecha otorgada
    '''

    if fecha is None: return {'error': errores['campo_obligatorio']}

    try:
        formato_fecha = '%d-%m-%Y'
        fecha = datetime.strptime(fecha, formato_fecha)

        dia = fecha.day
        mes = fecha.month
        anio = fecha.year

        data = obtener_datos_sii(anio)

        if type(data) == dict:
            return data
        
        return data[dia - 1][mes - 1]
    except ValueError:
        return {'error': errores['tipo_fecha']}
    

@app.get('/consulta-sii')
async def consulta_unidad_fomento(response: Response, fecha: Union[str, None] = None):
    '''
    Obtiene una fecha a través del Query Param: fecha
    retorna un JSON con el valor de la unidad
    '''
    try:
        valor_unidad = generar_unidades_fomento(fecha)
        if type(valor_unidad) != str:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return valor_unidad

        return {
            'fecha_ingresada': fecha,
            'valor_unidad_fomento': valor_unidad
        }
        
    except Exception:
        return {'error': errores['tipo_fecha']}
        