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
    Zobrazení stránky uživatele.
    Returns:
        HTML stránka s informacemi o uživatelském účtu.
    """

    users = execute('SELECT * FROM users')

    return render_template('default.html', users = users)

@bp.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete(user_id):
    """

    """
    command = "DELETE FROM users WHERE id = ? AND id != ?"

    execute(command, (user_id, session["id"]))
    flash("Uživatel byl úspěšně odtsraněn", "success")
    return redirect(url_for('playlist.index'))
