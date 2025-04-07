from flask import render_template, request, flash
from os import path
from app import create_app, auth, db, playlist, admin

app = create_app()
app.register_blueprint(auth.bp)
app.register_blueprint(playlist.bp)
app.register_blueprint(admin.bp)

if __name__ == '__main__':
    """
    Spustí aplikaci Flask a zajistí vytvoření databáze, pokud neexistuje.
    Returns:
        Nic
    """
    if not path.exists(app.config["DATABASE"]):
        with app.app_context():
            db.create_db()
    app.run(debug=True)
