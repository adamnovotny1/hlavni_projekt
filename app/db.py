import sqlite3
from flask import current_app

def create_db():
    """
    Vytvoří databázi podle schématu definovaného v DB_SCHEME.
    Returns:
        Nic
    """
    with sqlite3.connect(current_app.config["DATABASE"]) as conn:
        with open(current_app.config["DB_SCHEME"]) as scheme:
            conn.executescript(scheme.read())
        conn.commit()


def execute(command, params=None):
    """
    Provede SQL příkaz s volitelnými parametry.
    Args:
        command (str): SQL příkaz k vykonání.
        params (tuple, optional): Parametry pro SQL příkaz.

    Returns:
        Seznam výsledků dotazu, nebo prázdný seznam, pokud není žádný výsledek.
    """
    with sqlite3.connect(current_app.config["DATABASE"]) as conn:
        if params:
            result = conn.execute(command, params).fetchall()
        else:
            result = conn.execute(command).fetchall()
        conn.commit()
    return result
