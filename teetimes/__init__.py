import teetimes.tee_times_web
from flask import Flask, request, render_template, session, redirect, url_for
from teetimes.scrapers import MonarchBay, CoricaPark, LasPositas
import json
from datetime import datetime
import numpy as np
import pandas as pd

app = Flask(__name__)

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

app.config['SECRET_KEY'] = config['SECRET_KEY']

@app.route('/', methods=("POST", "GET"))
def home():
    if request.method == "POST":
        date = datetime.strptime(request.form["user-date"], '%Y-%m-%d')
        num_players = int(request.form["num-players"])
    elif request.method == "GET":
        date = datetime(2022, 10, 22)
        num_players = 0

    mb = MonarchBay(date, num_players)
    cp = CoricaPark(date, num_players)
    lp = LasPositas(date, num_players)

    html_tables = {
        "Monarch Bay": mb.tee_times.to_html(classes='data'),
        "Corica Park": cp.tee_times.to_html(classes='data'),
        "Las Positas": lp.tee_times.to_html(classes='data')
    }
    
    return render_template('home.html', tables=html_tables)

if __name__ == "__main__":
    app.run()