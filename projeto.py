from markupsafe import escape
from flask import Flask, render_template, redirect, url_for, request, session,make_response


app = Flask(__name__)

@app.route('/')
def home():
    anuncios = {
        "Eletrônicos": [
            {"id": 1, "titulo": "Smartphone", "descricao": "Um ótimo smartphone.", "preco": "R$ 1.200,00", "perguntas": ["Qual a capacidade da bateria?", "Vem com garantia?"]},
            {"id": 2, "titulo": "Laptop", "descricao": "Um excelente laptop.", "preco": "R$ 2.500,00", "perguntas": ["Qual o processador?", "Tem porta HDMI?"]},
            {"id": 3, "titulo": "Headphones", "descricao": "Headphones com cancelamento de ruído.", "preco": "R$ 300,00", "perguntas": ["Qual a autonomia da bateria?", "É compatível com iOS?"]},
            {"id": 4, "titulo": "Relógio Inteligente", "descricao": "Relógio inteligente com várias funcionalidades.", "preco": "R$ 400,00", "perguntas": ["É à prova d'água?", "Qual a duração da bateria?"]}
        ],
        "Móveis": [
            {"id": 5, "titulo": "Sofá", "descricao": "Sofá confortável de 3 lugares.", "preco": "R$ 1.500,00", "perguntas": ["Qual o material do sofá?", "É removível para lavagem?"]},
            {"id": 6, "titulo": "Mesa de Jantar", "descricao": "Mesa de jantar de madeira para 6 pessoas.", "preco": "R$ 800,00", "perguntas": ["Qual o tipo de madeira?", "Tem algum acabamento especial?"]},
            {"id": 7, "titulo": "Cadeira Escritório", "descricao": "Cadeira ergonômica para escritório.", "preco": "R$ 350,00", "perguntas": ["Qual a altura máxima da cadeira?", "Possui ajuste de apoio lombar?"]},
            {"id": 8, "titulo": "Estante", "descricao": "Estante de livros com 5 prateleiras.", "preco": "R$ 450,00", "perguntas": ["Qual a largura da estante?", "É fácil de montar?"]}
        ],
        "Roupas": [
            {"id": 9, "titulo": "Camisa Casual", "descricao": "Camisa casual de algodão.", "preco": "R$ 120,00", "perguntas": ["Qual o tamanho disponível?", "É pré-lavada?"]},
            {"id": 10, "titulo": "Calça Jeans", "descricao": "Calça jeans de corte reto.", "preco": "R$ 180,00", "perguntas": ["Qual o material do jeans?", "Tem opções de tamanho?"]},
            {"id": 11, "titulo": "Jaqueta de Couro", "descricao": "Jaqueta de couro genuíno.", "preco": "R$ 600,00", "perguntas": ["O couro é natural ou sintético?", "Qual a lavagem recomendada?"]},
            {"id": 12, "titulo": "Tênis Esportivo", "descricao": "Tênis esportivo para corrida.", "preco": "R$ 250,00", "perguntas": ["Qual o tipo de solado?", "É impermeável?"]}
        ],
        "Utensílios de Cozinha": [
            {"id": 13, "titulo": "Liquidificador", "descricao": "Liquidificador com 5 velocidades.", "preco": "R$ 200,00", "perguntas": ["Qual a capacidade do copo?", "É fácil de limpar?"]},
            {"id": 14, "titulo": "Panela de Pressão", "descricao": "Panela de pressão de 4 litros.", "preco": "R$ 150,00", "perguntas": ["Qual o material da panela?", "Pode ser usada em fogão indução?"]},
            {"id": 15, "titulo": "Torradeira", "descricao": "Torradeira com 2 fendas.", "preco": "R$ 120,00", "perguntas": ["Tem ajuste de intensidade de toste?", "Qual a potência?"]},
            {"id": 16, "titulo": "Cafeteira", "descricao": "Cafeteira elétrica com capacidade de 12 xícaras.", "preco": "R$ 180,00", "perguntas": ["Tem função de manter aquecido?", "Qual o material do filtro?"]}]
    }
    return render_template('home.html', anuncios=anuncios)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/minha-conta')
def minha_conta():
    return render_template('minha_conta.html')

@app.route('/anunciar')
def anunciar():
    return render_template('anunciar.html')

@app.route('/meusanuncios')
def meusanuncios():
    return render_template('meusanuncios.html')

@app.route('/favoritos')
def favoritos():
    return render_template('favoritos.html')

@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')




#######################################################
"""
@app.route('/cad/usuario')
def usuario():
    return render_template('usuario.html', titulo="Cadastro de usuário")

@app.route("/cad/caduser", methods=['POST'])
def caduser():
    return request.form

@app.route('/cad/anuncio')
def anuncio():
    return render_template('anuncio.html')

@app.route('/anuncios/pergunta')
def pergunta():
    return render_template('pergunta.html')

@app.route('/anuncios/compra')
def compra():
    print('anuncio comprado')
    return ''

@app.route('/anuncio/favoritos')
def favoritos():
    print('favorito inserido')
    return f'<h4>Comprado</h4>'

@app.route('/config/categoria')
def categoria():
    return render_template('categoria.html')

@app.route('/relatorios/vendas')
def relvendas():
    return render_template('relvendas.html')

@app.route('/relatorios/compras')
def relcompras():
    return render_template('relcompras.html')"""