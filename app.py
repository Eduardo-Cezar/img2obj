from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://edu:123@localhost/banco_notas'
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    notas = db.relationship('Nota', backref='usuario', lazy=True)

    def __init__(self, username, senha):
        self.username = username
        self.senha = generate_password_hash(senha)

class Nota(db.Model):
    __tablename__ = 'nota'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    conteudo = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect('/login')
    return redirect('/notas')

@app.route('/teste-db')
def teste_db():
    try:
        db.session.execute(text('SELECT * from nota'))
        return 'Conexão com banco de dados OK!'
    except Exception as e:
        return f'Erro na conexão: {str(e)}'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        # validacoes
        if len(username) < 3:
            flash('O nome de usuário deve ter pelo menos 3 caracteres')
            return redirect(url_for('register'))

        if len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres')
            return redirect(url_for('register'))

        if senha != confirmar_senha:
            flash('As senhas não coincidem')
            return redirect(url_for('register'))

        #verifica se o user existe
        usuario_existe = Usuario.query.filter_by(username=username).first()
        if usuario_existe:
            flash('Este nome de usuário já está em uso')
            return redirect(url_for('register'))

        try:
            #cria novo usuário
            novo_usuario = Usuario(username=username, senha=senha)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar usuário. Tente novamente.')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            return redirect(url_for('index'))
        
        flash('Nome de usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('login'))

with app.app_context():
    db.drop_all()  # Remove todas as tabelas
    db.create_all()  # recria com a estrutura definida
    print("Tabelas criadas com sucesso!")

if __name__ == '__main__':
    print("Servidor Flask iniciando...")
    try:
        app.run(debug=True)
        print("Servidor rodando em http://localhost:5000")
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {str(e)}")