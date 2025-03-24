from flask import Blueprint, render_template, session, flash, redirect

bp = Blueprint('library', __name__, url_prefix='/library')

@bp.route('/')
def index():
    if not "username" in session:
        flash()
        return render_template()