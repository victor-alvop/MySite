import requests
from flask import Blueprint, render_template, url_for, redirect
from datetime import datetime
from app.database.db_source import db, Crypto, CryptoActualPrice

crypto_info_bp = Blueprint('crypto_info', __name__)

@crypto_info_bp.route('/crypto-docs')
def cryptoDocs():
    return render_template('cryptoDocs.html')

@crypto_info_bp.route('/')
def cryptoInfo():

    crypto_items = Crypto.query.order_by(Crypto.date.desc()).all()

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
        data = response.json()

        for coin in data:
            iso_date = coin.get('last_updated')
            if iso_date:
                dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
                coin['formatted_date'] = dt.strftime('%d/%m/%Y')
            else:
                coin['formatted_date'] = 'N/A'

        return render_template('cryptoInfo.html', crypto_items=crypto_items, coins=data)
    except Exception as e:
        return render_template('cryptoInfo.html', coins={'error': str(e)})

############
@crypto_info_bp.route('/updateCyrpto', methods=["POST"])
def crypto_update():

    crypto_items = Crypto.query.all()

    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }
    excluded_names = ['USDC', 'Tether']


    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        for coin in data:
            iso_date = coin.get('last_updated')
            if iso_date:
                dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
                coin['formatted_date'] = dt.strftime('%d/%m/%Y')
            else:
                dt = datetime.utcnow()
                coin['formatted_date'] = 'N/A'


            if coin['name'] not in excluded_names:
                new_crypto = Crypto(
                    name=coin['name'],
                    symbol=coin['symbol'],
                    price=coin['current_price'],
                    date=dt
                )
                db.session.add(new_crypto)
            
            # 2. Actualizar tabla "CryptoActualPrice"
            crypto = CryptoActualPrice.query.filter_by(name=coin['name']).first()
            if crypto:
                crypto.price = coin['current_price']
                crypto.date = dt  # usamos la misma conversión
            else:
                    # Si no existe, puedes decidir crearla también
                new_actual = CryptoActualPrice(
                    name=coin['name'],
                    symbol=coin['symbol'],
                    price=coin['current_price'],
                    date=dt
                    )
                db.session.add(new_actual)

        db.session.commit()
        return redirect(url_for('crypto_info.cryptoInfo'))
    except Exception as e:
        return render_template('cryptoInfo.html', coins={'error': str(e)})