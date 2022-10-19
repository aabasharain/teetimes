from flask import Flask, request, render_template, session, redirect, url_for
from teetimes.scrapers import MonarchBay, CoricaPark, LasPositas
from datetime import datetime
import json
import numpy as np
import pandas as pd

app = Flask(__name__)

try:
    with open('/etc/config.json') as config_file:
        config = json.load(config_file)

    app.config['SECRET_KEY'] = config['SECRET_KEY']
except Exception as e:
    print('no secret key found')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/teetimes', methods=("POST", "GET"))
def tee_times():
    if request.method == "POST":
        try:
            date = datetime.strptime(request.form["user-date"], '%Y-%m-%d')
        except ValueError as e:
            date = datetime.now()
        num_players = int(request.form["num-players"])
    elif request.method == "GET":
        date = datetime.now()
        num_players = 4

    mb = MonarchBay(date, num_players)
    cp = CoricaPark(date, num_players)
    lp = LasPositas(date, num_players)

    html_tables = {
        "Monarch Bay": mb.tee_times.to_html(classes='data'),
        "Corica Park": cp.tee_times.to_html(classes='data'),
        "Las Positas": lp.tee_times.to_html(classes='data')
    }
    
    return render_template('teetimes.html', tables=html_tables)# mb_table.to_html(classes='data')])#, titles=data.columns.values)#data.columns.values) # to_html(classes='data')], titles=df.columns.values)
    # else:
    #     return render_template('home.html', tables={})#, titles="None Available")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)