from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import MetaData


import json

app = Flask(__name__)

sql_user = "default"
sql_user = "password"
sql_host = "localhost"
sql_host = "5432"
sql_db_name = "flask"
sql_schema_name = "public"

with open("credentials.json", "r") as creds_file:
    creds = json.load(creds_file)
    sql_user = creds["sql"]["username"]
    sql_password = creds["sql"]["password"]
    sql_host = creds["sql"]["host"]
    sql_port = creds["sql"]["port"]
    sql_db_name = creds["sql"]["db_name"]
    sql_schema_name = creds["sql"]["schema_name"]

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{sql_user}:{sql_password}@{sql_host}:{sql_port}/{sql_db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

metadata = MetaData(schema=sql_schema_name)

db = SQLAlchemy(app=app, metadata=metadata)

from ecoround.models import match
from ecoround.views import kills, saveround

with app.app_context():
    db.create_all()
