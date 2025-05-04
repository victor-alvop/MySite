from flask import Flask, render_template, jsonify
import requests

def api_consult():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # lanza excepción si la respuesta no es 200
        data = response.json()
        return data
    except Exception as e:
        return {'error': str(e)}

# Llamada de prueba
result = api_consult()
print(result)