from plistlib import dumps
from flask import Blueprint, render_template, request, session, flash, url_for, redirect
from functools import wraps
from app.db import execute

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Obsluhuje přihlášení uživatele.
    Returns:
        HTML stránka s přihlášením nebo přesměrování na hlavní stránku.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        command = "SELECT user, role, id FROM users WHERE user = ? AND password = ?"

        result = execute(command, (username, password))

        if result:
            session["username"] = username
            session["role"] = "admin"
            session["id"] = result[0][2]

            flash("Login succesful")
            return redirect(url_for('index'))
        else:
            flash("Login unsuccessful", "warning")

    return render_template("login.html")


@bp.route('/logout')
def logout():
    """
    Obsluhuje odhlášení uživatele.
    Returns:
        Přesměrování na hlavní stránku po odhlášení.
    """
    session.pop('username', None)
    session.pop('role', None)
    session.pop('id', None)
    flash("Byl jsi odhlášen")
    return redirect(url_for('index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Obsluhuje registraci nového uživatele.
    Returns:
        HTML stránka pro registraci nebo přesměrování na přihlašovací stránku.
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        error = False

        if password != password2:
            error = True
            flash("Hesla se neshodují", "warning")

        command = "SELECT user FROM users WHERE user = ?"
        if execute(command, (username,)):
            error = True
            flash("Uživatelské jméno již existuje", "error")

        command = "SELECT email FROM users WHERE email = ?"
        if execute(command, (email,)):
            error = True
            flash("Email již existuje", "error")

        if not error:
            command = "INSERT INTO users (user, email, password) VALUES (?, ?, ?)"
            execute(command, (username, email, password))
            flash("Registrace probíhla úspěšně", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Registrace neprobíhla úspěšně", "error")

    return render_template('register.html')

def login_required(func):
    """
    Dekorátor pro ochranu stránek, které jsou dostupné pouze pro přihlášené uživatele.
    Args:
        Funkce, kterou chceme chránit před přístupem nepřihlášených uživatelů.

    Returns:
        Wrapper, který buď zavolá původní funkci, nebo přesměruje uživatele.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("Sekce pro přihlášené uživatele")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    """
    Dekorátor pro ochranu stránek, které jsou dostupné pouze pro přihlášené uživatele.
    Args:
        Funkce, kterou chceme chránit před přístupem nepřihlášených uživatelů.

    Returns:
        Wrapper, který buď zavolá původní funkci, nebo přesměruje uživatele.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session["role"] != "admin" :
            flash("Sekce pouze pro Administrátora", "error")
            return redirect(url_for("index"))
        return func(*args, **kwargs)
    return wrapper

@bp.route('/user')
def user():
    """
    Zobrazení stránky uživatele.
    Returns:
        HTML stránka s informacemi o uživatelském účtu.
    """
    return render_template("user.html")
