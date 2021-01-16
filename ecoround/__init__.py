from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import json

app = Flask(__name__)

sql_user = "default"
sql_user = "password"
sql_host = "localhost"
sql_host = "5432"
sql_db_name = "flask"

with open("credentials.json", "r") as creds_file:
    creds = json.load(creds_file)
    sql_user = creds["sql"]["username"]
    sql_password = creds["sql"]["password"]
    sql_host = creds["sql"]["host"]
    sql_port = creds["sql"]["port"]
    sql_db_name = creds["sql"]["db_name"]


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{sql_user}:{sql_password}@{sql_host}:{sql_port}/{sql_db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
result = db.session.execute("\dt")
print(result)
migrate = Migrate(app, db)

from ecoround.models import match
from ecoround.views import kills, saveround
