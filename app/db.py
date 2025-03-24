import sqlite3
from flask import current_app

def create_db():
    with sqlite3.connect(current_app.config["DATABASE"]) as conn:
        with open(current_app.config["DB_SCHEME"]) as scheme:
            conn.executescript(scheme.read())
        conn.commit()

def execute(command, params=None):
    with sqlite3.connect(current_app.config["DATABASE"]) as conn:
        if params:
            result = conn.execute(command, params).fetchall()
        else:
            result = conn.execute(command).fetchall()
        conn.commit()
    return result

