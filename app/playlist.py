from flask import Blueprint, render_template, session, flash, redirect, url_for
from app.auth import login_required

bp = Blueprint('playlist', __name__, url_prefix='/playlist')

@bp.route('/')
@login_required
def index():
    return render_template('playlist.html')