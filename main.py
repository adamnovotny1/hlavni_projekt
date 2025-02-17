from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'heslo':
            return render_template('login.html', login = True)
        else:
            return render_template('login.html', login = False)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
