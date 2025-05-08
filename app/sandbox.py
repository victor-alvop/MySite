'''
import yfinance as yf
from datetime import datetime, timedelta
from flask import render_template
from app.database.db_source import db, Crypto

def cryptoInfo():
    crypto_items = Crypto.query.order_by(Crypto.date.desc()).all()

    # Mapeo de nombres → símbolos de yfinance
    tickers = {
        'Ethereum': 'ETH-USD',
        'Tether': 'USDT-USD',
        'Bitcoin': 'BTC-USD',
        'USDC': 'USDC-USD',
        'TRON': 'TRX-USD',
        'Solana': 'SOL-USD',
        'BNB': 'BNB-USD',
        'Cardano': 'ADA-USD',
        'Dogecoin': 'DOGE-USD',
        'XRP': 'XRP-USD'
    }

    coins = []

    try:
        # Rango de fecha: ayer hasta hoy (para evitar errores de horario)
        end_date = '2022-02-01'
        start_date = '2022-01-01'

        for name, ticker in tickers.items():
            df = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)

            if not df.empty:
                close_price = df['Close'][-1]
                last_date = df.index[-1].date()

                # Evitar duplicados
                exists = Crypto.query.filter_by(name=name, date=last_date).first()
                if not exists:
                    new_crypto = Crypto(name=name, price=close_price, date=last_date)
                    db.session.add(new_crypto)

                # Agregar a la vista
                coins.append({
                    'name': name,
                    'price': close_price,
                    'formatted_date': last_date.strftime('%d/%m/%Y')
                })

        db.session.commit()
        return render_template('cryptoInfo.html', crypto_items=crypto_items, coins=coins)

    except Exception as e:
        return render_template('cryptoInfo.html', coins={'error': str(e)})


cryptoInfo()
'''