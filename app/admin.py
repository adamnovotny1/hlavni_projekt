from flask import Blueprint, render_template, request, session, flash, url_for, redirect
from app.auth import login_required, admin_required
from functools import wraps
from app.db import execute

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/default')
@login_required
@admin_required
def default():

    """
    Zobrazení stránky s výpisem uživatelů.
    Returns:
        HTML stránka s informacemi o uživatelském účtě.
    """

    users = execute('SELECT * FROM users')

    return render_template('default.html', users = users)

@bp.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def delete(user_id):
    """
    Stránka pro úpravu uživatele s doplňenými údaji.
    Returns:
        vrácení na stránku s výpisem uživatelů.

    """
    command = "DELETE FROM users WHERE id = ? AND id != ?"

    execute(command, (user_id, session["id"]))
    flash("Uživatel byl úspěšně odtsraněn", "success")
    return redirect(url_for('playlist.index'))

@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_user(user_id):
    """
    Stránka pro úpravu uživatele s doplňenými údaji.

    Returns:
        vrácení na zpět
        vygenerování formuláře pro editaci uživatele

    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']

        command = """
            UPDATE users
            SET user = ?, email = ?, role = ?, password = ?
            WHERE id = ?
        """

        execute(command, (username, email, role, password,user_id,))
        flash("Uživatel byl úspěšně upraven", "success")
        return redirect(url_for('admin.default'))

    user = execute("SELECT * FROM users WHERE id = ? ", (user_id,))
    if not user:
        flash("Uživatel nebyl nalezen", "error")
        return redirect(url_for('admin.default'))

    return render_template('edit_user.html', user = user)