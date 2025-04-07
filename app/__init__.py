from flask import Flask, render_template

def create_app():
    """
        Vytvoří a nakonfiguruje aplikaci Flask.
        Returns:
            Instance Flask aplikace s nastavenými konfiguracemi a definovanou hlavní routou.
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config["SECRET_KEY"] = "development key"
    app.config["DATABASE"] = "database.sqlite"
    app.config["DB_SCHEME"] = "scheme.sql"

    @app.route('/')
    def index():
        """
        Zobrazení hlavní stránky aplikace.
        Returns:
            HTML stránka generovaná šablonou `index.html`.
        """
        return render_template('index.html')

    return app
