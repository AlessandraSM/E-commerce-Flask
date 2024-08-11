from flask import Flask, render_template, request, session, make_response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz


app = Flask(__name__)
app.secret_key = '12345678'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://alessandra:alessandra@localhost:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column('id_usuario', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column('nome', db.String(255), nullable=False)
    email = db.Column('email', db.String(100), nullable=False, unique=True)
    cpf = db.Column('cpf', db.String(14), nullable=False, unique=True)
    endereco = db.Column('endereco', db.String(100), nullable=True)
    senha = db.Column('senha', db.String(255), nullable=False)
    tipo_usuario = db.Column('tipo_usuario', db.Enum('física', 'jurídica', name='tipo_usuario_enum'), nullable=False)

    def __init__(self, nome, email, cpf, senha, endereco=None, tipo_usuario='física'):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.senha = senha
        self.endereco = endereco
        self.tipo_usuario = tipo_usuario


class Categoria(db.Model):
    __tablename__ = 'categoria'
    
    id_categoria = db.Column('id_categoria', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column('nome', db.String(45), nullable=False)

    def __init__(self, nome):
        self.nome = nome

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id_produtos = db.Column('id_produtos', db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column('titulo', db.String(45), nullable=False)
    descricao = db.Column('descricao', db.String(250), nullable=False)
    preco = db.Column('preco', db.Numeric(8, 2), nullable=False)
    marca = db.Column('marca', db.String(45), nullable=True)
    modelo = db.Column('modelo', db.String(100), nullable=True)
    url_imagem = db.Column('url_imagem', db.String(255), nullable=True)
    condicao = db.Column('condicao', db.String(10), nullable=True)
    id_tipo_categoria = db.Column('id_tipo_categoria', db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    id_vendedor = db.Column('id_vendedor', db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    
    categoria = db.relationship('Categoria', backref=db.backref('produtos', lazy=True))
    vendedor = db.relationship('Usuario', backref=db.backref('produtos', lazy=True))

    def __init__(self, titulo, descricao, preco, marca, modelo, url_imagem, condicao, id_tipo_categoria, id_vendedor):
        self.titulo = titulo
        self.descricao = descricao
        self.preco = preco
        self.marca = marca
        self.modelo = modelo
        self.url_imagem = url_imagem
        self.condicao = condicao
        self.id_tipo_categoria = id_tipo_categoria
        self.id_vendedor = id_vendedor


class Pedido(db.Model):
    __tablename__ = 'pedido'
    
    id_pedido = db.Column('id_pedido', db.Integer, primary_key=True, autoincrement=True)
    data = db.Column('data', db.Date, nullable=False)
    status = db.Column('status', db.String(45), nullable=False)
    id_comprador = db.Column('id_comprador', db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    
    comprador = db.relationship('Usuario', backref=db.backref('pedidos', lazy=True))

    def __init__(self, data, status, id_comprador):
        self.data = data
        self.status = status
        self.id_comprador = id_comprador

class ItemPedido(db.Model):
    __tablename__ = 'item_pedido'
    
    id_item_pedido = db.Column('id_item_pedido', db.Integer, primary_key=True, autoincrement=True)
    quantidade = db.Column('quantidade', db.Integer, nullable=False)
    preco_unidade = db.Column('preco_unidade', db.Numeric(8, 2), nullable=False)
    id_do_pedido = db.Column('id_do_pedido', db.Integer, db.ForeignKey('pedido.id_pedido'), nullable=False)
    id_do_produto = db.Column('id_do_produto', db.Integer, db.ForeignKey('produtos.id_produtos'), nullable=False)
    
    pedido = db.relationship('Pedido', backref=db.backref('itens', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('itens', lazy=True))

    def __init__(self, quantidade, preco_unidade, id_do_pedido, id_do_produto):
        self.quantidade = quantidade
        self.preco_unidade = preco_unidade
        self.id_do_pedido = id_do_pedido
        self.id_do_produto = id_do_produto

class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    
    id_favoritos = db.Column('id_favoritos', db.Integer, primary_key=True, autoincrement=True)
    data_favoritado = db.Column('data_favoritado', db.Date, nullable=False)
    id_usuario_favoritou = db.Column('id_usuario_favoritou', db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_produto_favoritado = db.Column('id_produto_favoritado', db.Integer, db.ForeignKey('produtos.id_produtos'), nullable=False)
    
    usuario = db.relationship('Usuario', backref=db.backref('favoritos', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('favoritos', lazy=True))

    def __init__(self, data_favoritado, id_usuario_favoritou, id_produto_favoritado):
        self.data_favoritado = data_favoritado
        self.id_usuario_favoritou = id_usuario_favoritou
        self.id_produto_favoritado = id_produto_favoritado


class Perguntas(db.Model):
    __tablename__ = 'perguntas'
    
    id_pergunta = db.Column('id_pergunta', db.Integer, primary_key=True, autoincrement=True)
    pergunta = db.Column('pergunta', db.String(45), nullable=False)
    data_pergunta = db.Column('data_pergunta', db.Date, nullable=False)
    resposta = db.Column('resposta', db.String(250), nullable=True)
    data_resposta = db.Column('data_resposta', db.Date, nullable=True)
    id_produto_pergunta = db.Column('id_produto_pergunta', db.Integer, db.ForeignKey('produtos.id_produtos'), nullable=False)
    id_usuario_pergunta = db.Column('id_usuario_pergunta', db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    
    produto = db.relationship('Produto', backref=db.backref('perguntas', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('perguntas', lazy=True))

    def __init__(self, pergunta, data_pergunta, resposta, data_resposta, id_produto_pergunta, id_usuario_pergunta):
        self.pergunta = pergunta
        self.data_pergunta = data_pergunta
        self.resposta = resposta
        self.data_resposta = data_resposta
        self.id_produto_pergunta = id_produto_pergunta
        self.id_usuario_pergunta = id_usuario_pergunta


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

from flask import session

@app.route('/')
def home():
    # Obtém todos os produtos
    produtos = Produto.query.all()
    categorias = Categoria.query.all()
# Obtém todos os IDs dos produtos comprados
    produtos_comprados_ids = (
        db.session.query(ItemPedido.id_do_produto)
        .join(Pedido, Pedido.id_pedido == ItemPedido.id_do_pedido)
        .filter(Pedido.status == 'Finalizado')  # Certifica-se de que estamos pegando apenas pedidos finalizados
        .distinct()
        .all()
    )
    produtos_comprados_ids = {produto_id for (produto_id,) in produtos_comprados_ids}

    # Filtra os produtos que não foram comprados
    produtos_disponiveis = [produto for produto in produtos if produto.id_produtos not in produtos_comprados_ids]

    # Organiza os produtos por categoria
    produtos_por_categoria = {cat.nome: [] for cat in categorias}
    for produto in produtos_disponiveis:
        categoria_nome = Categoria.query.filter_by(id_categoria=produto.id_tipo_categoria).first().nome
        produtos_por_categoria[categoria_nome].append(produto)

    # Obtém o ID do usuário da sessão
    user_id = session.get('user_id', None)

    return render_template('home.html', anuncios=produtos_por_categoria, user_id=user_id)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.senha == senha:
            session['user_id'] = usuario.id_usuario
            return redirect(url_for('minha_conta', user_id=usuario.id_usuario))
        else:
            return 'Credenciais inválidas!'
    
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastro/usuario', methods=['POST'])
def cadastro_usuario():
    usuario = Usuario(
        nome=request.form.get('nome'),
        email=request.form.get('email'),
        cpf=request.form.get('cpf'),
        endereco=request.form.get('endereco'),
        senha=request.form.get('senha'),
        tipo_usuario=request.form.get('tipo_usuario')
    )
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/usuario/<int:id>')
def get_user(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route('/editar/<int:id>', methods=["GET", "POST"])
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.cpf = request.form['cpf']
        usuario.endereco = request.form['endereco']
        usuario.senha = request.form['senha']
        usuario.tipo_usuario = request.form['tipo_usuario']
        try:
            db.session.commit()
            return redirect('/admin')
        except:
            return 'There was a problem updating the user'
    else:
        return render_template('editar.html', usuario=usuario)

@app.route('/usuario/delete/<int:id>')
def delete_user(id):
    usuario = Usuario.query.get_or_404(id)
    try:
        db.session.delete(usuario)
        db.session.commit()
        return redirect('/admin')
    except:
        return 'There was a problem deleting that user'

@app.route('/admin')
def admin():
    usuarios = Usuario.query.all()
    return render_template('admin.html', usuarios=usuarios)

@app.route('/minha_conta/<int:user_id>')
def minha_conta(user_id):
    return render_template('minha_conta.html', user_id=user_id)


@app.route('/anunciar/<int:id>', methods=['GET', 'POST'])
def anunciar(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        preco = request.form['preco']
        marca = request.form['marca']
        modelo = request.form['modelo']
        url_imagem = request.form['imagem']
        condicao = request.form['condicao']
        id_categoria = request.form['categoria']
        id_vendedor = id  # Usar o ID passado na URL

        novo_produto = Produto(
            titulo=titulo, descricao=descricao, preco=preco, marca=marca,
            modelo=modelo, url_imagem=url_imagem, condicao=condicao,
            id_tipo_categoria=id_categoria, id_vendedor=id_vendedor
        )

        db.session.add(novo_produto)
        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template('anunciar.html', user_id=id)

@app.route('/meus_anuncios/<int:user_id>')
def meus_anuncios(user_id):
    produtos = Produto.query.filter_by(id_vendedor=user_id).all()
    return render_template('meus_anuncios.html', produtos=produtos, user_id=user_id)


@app.route('/delete_produto/<int:produto_id>', methods=['POST'])
def delete_produto(produto_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    produto = Produto.query.get(produto_id)
    if produto and produto.id_vendedor == user_id:
        db.session.delete(produto)
        db.session.commit()
    return redirect(url_for('meus_anuncios', user_id=user_id))

@app.route('/comprar/<int:id_produto>', methods=['POST'])
def comprar(id_produto):
    produto = Produto.query.get(id_produto)
    
    if not produto:
        return "Produto não encontrado", 404
    
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']

    utc_now = datetime.now(pytz.utc)

    novo_pedido = Pedido(data=utc_now, status='Finalizado', id_comprador=user_id)
    db.session.add(novo_pedido)
    db.session.commit()
    
    item_pedido = ItemPedido(
        quantidade=1,  
        preco_unidade=produto.preco,
        id_do_pedido=novo_pedido.id_pedido,
        id_do_produto=produto.id_produtos
    )
    db.session.add(item_pedido)
    db.session.commit()
    
    return redirect(url_for('home'))


@app.route('/favoritos')
def favoritos():
    return render_template('favoritos.html')

@app.route('/relatorio/<int:user_id>')
def relatorio(user_id):
    # Obtém todos os produtos comprados pelo usuário
    produtos_comprados = (
        db.session.query(Produto, Pedido.data)
        .join(ItemPedido, ItemPedido.id_do_produto == Produto.id_produtos)
        .join(Pedido, Pedido.id_pedido == ItemPedido.id_do_pedido)
        .filter(Pedido.id_comprador == user_id)
        .all()
    )

    # Obtém todos os produtos vendidos pelo usuário
    produtos_vendidos = (
        db.session.query(Produto, Pedido.data)
        .join(ItemPedido, ItemPedido.id_do_produto == Produto.id_produtos)
        .join(Pedido, Pedido.id_pedido == ItemPedido.id_do_pedido)
        .filter(Produto.id_vendedor == user_id)
        .all()
    )
    
    # Calcula o lucro total de vendas
    lucro_total = sum(
        item.preco_unidade * item.quantidade
        for produto, pedido_data in produtos_vendidos
        for item in ItemPedido.query.filter_by(id_do_produto=produto.id_produtos).all()
    )

    return render_template(
        'relatorio.html',
        produtos_comprados=produtos_comprados,
        produtos_vendidos=produtos_vendidos,
        lucro_total=lucro_total
    )


if __name__ == 'projeto':
    print('entrou')
    with app.app_context():
        print('criou')
        db.create_all()
    app.run()
