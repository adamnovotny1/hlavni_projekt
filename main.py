from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'heslo':
            flash("Úspěšné přihlášení")
            return render_template('login.html', login = True)
        else:
            flash("Přihlášení neproběhlo úspěšně", "warning")
            return render_template('login.html', login = False)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
