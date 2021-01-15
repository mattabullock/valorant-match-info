from flask import Flask

app = Flask(__name__)

from ecoround.views import kills, saveround
