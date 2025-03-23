from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


def init_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'heslo':
            return render_template('login.html', login=True)
        else:
            return render_template('login.html', login=False)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return "Tento e-mail je již zaregistrován"

        new_user = User(name=name, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html')

    return render_template('register.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
