from flask import Flask
from markupsafe import escape
from flask import render_template


app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/bemvindo')
def bemvindo():
    return "<p>Seja bem vindo ao site de vendas!</p>"

@app.route('/sobre/privacidade')
def privacidade():
    return "<p>Seus dados estão seguros aqui</p>"


@app.route('/user/<username>')
def username(username):
    print('o que foi passado', username)
    return f"<h1>{escape(username)}</h1>"

@app.route('/teste')
def teste():
    return render_template('index.html')


