from flask import Flask, render_template

def create_app():
    app = Flask(__name__,template_folder='../templates',static_folder='../static')
    app.config["SECRET_KEY"] = "development key"
    app.config["DATABASE"] = "database.sqlite"
    app.config["DB_SCHEME"] = "scheme.sql"

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
