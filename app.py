from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import time
from sqlalchemy_utils import database_exists, create_database, drop_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://edu:123@localhost/banco_notas'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# garante que a pasta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    imagens = db.relationship('Imagem', backref='usuario', lazy=True)

    def __init__(self, username, senha):
        self.username = username
        self.senha = generate_password_hash(senha)

class Imagem(db.Model):
    __tablename__ = 'imagem'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    arquivo = db.Column(db.String(255), nullable=False)
    objeto_3d = db.Column(db.String(255))
    nome_objeto = db.Column(db.String(100))  # Nome do objeto 3D
    tempo_conversao = db.Column(db.Float)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

with app.app_context():
    # cria todas as tabelas se não existirem
    db.create_all()
    print("Tabelas verificadas/criadas com sucesso!")

@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

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

        # validações
        if len(username) < 3:
            flash('O nome de usuário deve ter pelo menos 3 caracteres')
            return redirect(url_for('register'))

        if len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres')
            return redirect(url_for('register'))

        if senha != confirmar_senha:
            flash('As senhas não coincidem')
            return redirect(url_for('register'))

        # verifica se user já  existe
        usuario_existe = Usuario.query.filter_by(username=username).first()
        if usuario_existe:
            flash('Este nome de usuário já está em uso')
            return redirect(url_for('register'))

        try:
            # cria  usuário
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
            return redirect(url_for('dashboard'))
        
        flash('Nome de usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(session['usuario_id'])
    imagens = Imagem.query.filter_by(usuario_id=session['usuario_id']).order_by(Imagem.data_upload.desc()).all()
    return render_template('dashboard.html', usuario=usuario, imagens=imagens)

@app.route('/upload', methods=['GET', 'POST'])
def upload_imagem():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'imagem' not in request.files:
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        
        file = request.files['imagem']
        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario_id']))
            os.makedirs(user_folder, exist_ok=True)
            
            filepath = os.path.join(user_folder, filename)
            file.save(filepath)
            
            # cria um novo registro no bd
            nova_imagem = Imagem(
                titulo=request.form.get('titulo', 'Sem título'),
                descricao=request.form.get('descricao', ''),
                arquivo=filepath,
                usuario_id=session['usuario_id']
            )
            
            db.session.add(nova_imagem)
            db.session.commit()
            
            flash('Imagem enviada com sucesso!')
            return redirect(url_for('dashboard'))

    return render_template('upload.html')

@app.route('/converter/<int:imagem_id>', methods=['POST'])
def converter_3d(imagem_id):
    if 'usuario_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    
    try:
        imagem = Imagem.query.get_or_404(imagem_id)
        if imagem.usuario_id != session['usuario_id']:
            return jsonify({'error': 'Acesso não autorizado'}), 403
        
        data = request.get_json()
        nome_objeto = data.get('nome_objeto')
        
        # remove a extensão .obj se o usuário incluiu
        if nome_objeto.lower().endswith('.obj'):
            nome_objeto = nome_objeto[:-4]
        
        if not nome_objeto:
            return jsonify({'error': 'Nome do objeto é obrigatório'}), 400
        
        print(f"Iniciando conversão da imagem {imagem_id} para objeto '{nome_objeto}'")
        
        tempo_inicio = time.time()
        
        input_path = os.path.join(os.getcwd(), imagem.arquivo)
        output_dir = os.path.join(
            app.config['UPLOAD_FOLDER'], 
            str(session['usuario_id']), 
            'objetos_3d'
        )
        
        print(f"Caminho da imagem: {input_path}")
        print(f"Diretório de saída: {output_dir}")
        
        # cria o diretório para objetos 3D se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            from imagem_objeto.img2obj import converter
            resultado = converter(input_path, nome_objeto, output_dir)
            print(f"Resultado da conversão: {resultado}")
            
            output_path = os.path.join(output_dir, f"{nome_objeto}.obj")
            
            tempo_fim = time.time()
            tempo_total = tempo_fim - tempo_inicio
            
            # Atualiza o banco de dados
            imagem.objeto_3d = output_path
            imagem.nome_objeto = nome_objeto  # salvando sem a extensao !!!!
            imagem.tempo_conversao = tempo_total
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': 'Conversão realizada com sucesso',
                'tempo': tempo_total
            })
            
        except Exception as e:
            print(f"Erro na função de conversão: {str(e)}")
            return jsonify({'error': f'Erro na conversão: {str(e)}'}), 500
            
    except Exception as e:
        print(f"Erro geral: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/deletar-imagem/<int:imagem_id>', methods=['DELETE'])
def deletar_imagem(imagem_id):
    if 'usuario_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    
    try:
        imagem = Imagem.query.get_or_404(imagem_id)
        
        # verifica se a imagem pertence ao usuário
        if imagem.usuario_id != session['usuario_id']:
            return jsonify({'error': 'Acesso não autorizado'}), 403
        
        # remove o arquivo da imagem
        if imagem.arquivo and os.path.exists(imagem.arquivo):
            os.remove(imagem.arquivo)
        
        #remove o arquivo do objeto 3D se existir
        if imagem.objeto_3d and os.path.exists(imagem.objeto_3d):
            os.remove(imagem.objeto_3d)
        
        #remove o registro do banco de dados
        db.session.delete(imagem)
        db.session.commit()
        
        return jsonify({'message': 'Imagem excluída com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Servidor Flask iniciando...")
    try:
        app.run(debug=True)
        print("Servidor rodando em http://localhost:5000")
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {str(e)}")