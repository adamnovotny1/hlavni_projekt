from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from app.auth import login_required
from app.db import execute

bp = Blueprint('playlist', __name__, url_prefix='/playlist')


@bp.route('/')
@login_required
def index():
    username = session["username"]
    """
    Zobrazení zabezpečené stránky aplikace pouze pro přihlášené uživatele.
        Returns:
            HTML stránka generovaná šablonou `playlist.html`.
    """

    user_id = session["id"]

    songs = execute('SELECT * FROM playlist WHERE user_id = ?', (user_id,))

    return render_template('playlist.html', songs=songs, username=username)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    Obsluhuje přidání nové písničky.
    Returns:
        HTML stránka pro přidání písničky nebo přesměrování na přidávací stránku.
    """
    if request.method == 'POST':
        name = request.form['name']
        artist = request.form['artist']
        album = request.form['album']
        genre = request.form['genre']
        user_id = session['id']

        command = "INSERT INTO playlist (name, artist, album, genre, user_id) VALUES (?, ?, ?, ?, ?)"
        execute(command, (name, artist, album, genre, user_id))
        flash("Písnička byla úspěšně přidána", "success")
        return redirect(url_for('playlist.index'))

    return render_template('add.html')


@bp.route('/delete/<int:song_id>', methods=['GET', 'POST'])
@login_required
def delete(song_id):
    """
        Obsluhuje smazání písničky.
        Returns:
            přesměrování na playlist stránku.
        """
    song = execute('SELECT * FROM playlist WHERE user_id = ? AND id = ?', (user_id,song_id,))
    print(song)
    command = "DELETE FROM playlist WHERE id = ? AND user_id = ?"

    execute(command, (song_id, session["id"]))
    flash("Písnička byla úspěšně odstraněna", "success")
    return redirect(url_for('playlist.index'))


@bp.route('/edit/<int:song_id>', methods=['GET', 'POST'])
@login_required
def edit(song_id):
    """
        Stránka pro úpravu písničky s doplňenými hodnotami.

        Returns:
            vrácení na zpět
            vygenerování formuláře pro editaci písničky

        """
    user_id = session["id"]
    song = execute('SELECT * FROM playlist WHERE user_id = ? AND id = ?', (user_id, song_id,))

    if song and song[0][5] != user_id:
        flash("Toto není vaše písnička", "error")
        return redirect(url_for('playlist.index'))

    if request.method == 'POST':
        name = request.form['name']
        artist = request.form['artist']
        album = request.form['album']
        genre = request.form['genre']

        command = """
            UPDATE playlist
            SET name = ?, artist = ?, album = ?, genre = ?
            WHERE id = ? 
            AND user_id = ?
        """

        execute(command, (name, artist, album, genre, song_id, session["id"]))
        flash("Písnička byla úspěšně upravena", "success")
        return redirect(url_for('playlist.index'))

    song = execute("SELECT * FROM playlist WHERE id = ? AND user_id = ?", (song_id,session["id"]))
    if not song:
        flash("Písnička nebyla nalezena", "error")
        return redirect(url_for('playlist.index'))

    return render_template('edit.html', song = song)
