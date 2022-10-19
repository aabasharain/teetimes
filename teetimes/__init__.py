import teetimes.tee_times_web
from flask import Flask
import json

app = Flask(__name__)

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

app.config['SECRET_KEY'] = config['SECRET_KEY']

if __name__ == "__main__":
    app.run()