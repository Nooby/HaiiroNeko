from datetime import datetime, timedelta

from flask import render_template, jsonify

from web import app
from database import Ticks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/db_info')
def db_info():
    size = Ticks.count()

    if size == 0:
        return jsonify({'db_size': 0})

    created = Ticks.oldest()
    modified = Ticks.newest()

    model = {'db_size': size,
             'db_created': created['Time'],
             'db_modified': modified['Time']}
    return jsonify(model)

@app.route('/exchange/<name>')
def exchange(name):
    ticker = Ticks.get_spot(name, datetime.utcnow() + timedelta(hours=-1))

    model = []
    for tick in ticker:
        model.append([tick['Time'].isoformat(), tick['Spot'], tick['Bid'], tick['Ask']])

    return jsonify(result = model)


@app.route('/exchanges')
def exchanges():
    exchanges = Ticks.get_exchange_names()
    return jsonify(result = exchanges)


