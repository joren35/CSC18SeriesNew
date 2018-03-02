from flask import Flask,jsonify
import requests

app = Flask(__name__)

@app.route('/')
def bitcoin_value():
    r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    time = r.json()['time']['updated']
    current_value = [r.json()['bpi']['USD'],r.json()['bpi']['GBP'],r.json()['bpi']['EUR']]
    return jsonify({'Time Updated': time,'Current value': current_value})

if __name__ == '__main__':
    app.run(debug=True)