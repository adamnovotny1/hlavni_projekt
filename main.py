from flask import render_template, request, flash
from os import path
from app import create_app, auth, db, playlist

app = create_app()
app.register_blueprint(auth.bp)
app.register_blueprint(playlist.bp)


if __name__ == '__main__':
    if not path.exists(app.config["DATABASE"]):
        with app.app_context():
            db.create_db()
    app.run(debug=True)
