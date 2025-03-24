from plistlib import dumps

from flask import Blueprint, render_template, request, session, flash, url_for, redirect
from app.db import execute

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        command = "SELECT user FROM users WHERE user = ? AND password = ?"

        result = execute(command, (username, password))

        if result:
            session["username"] = username
            flash("Login succesful")
        else:
            flash("Login unsuccessful","warning")
    return render_template("login.html")

@bp.route('/logout')
def logout():
    session.pop('username', None)
    flash("Byl jsi odhlášen")
    return redirect(url_for('index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        error = False

        if password != password2:
            error = True
            flash("Hesla se neshodují","warning")

        command = "SELECT user FROM users WHERE user = ?"
        if execute(command, (username,)):
            error = True
            flash("Uživatelské jméno již existuje","error")

        command = "SELECT email FROM users WHERE user = ?"
        if execute(command, (email,)):
            error = True
            flash("Email již existuje", "error")
        dumps(error)
        if not error:
            command = "INSERT INTO users (user, email, password) VALUES (?, ?, ?)"
            execute(command, (username, email, password))
            flash("registrace proběhla úspěšně","success")
            return redirect(url_for('auth.login'))
        else:
            flash("registrace neproběhla úspěšně","error")

    return render_template('register.html')
