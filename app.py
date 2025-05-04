import os
import json
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = 'static/img'
DADOS_JSON = 'dados_imagens.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verifica se o arquivo tem extensão válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Página inicial
@app.route('/')
def home():
    return render_template('home.html')

# Página "Sobre"
@app.route('/sobre')
def sobre():
    imagens = []
    for nome_arquivo in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(nome_arquivo):
            imagens.append(nome_arquivo)
    return render_template('sobre.html', imagens=imagens)

# Página de conteúdos (galeria)
@app.route('/conteudos')
def conteudos():
    if os.path.exists(DADOS_JSON):
        with open(DADOS_JSON, 'r', encoding='utf-8') as f:
            imagens = json.load(f)
    else:
        imagens = []
    return render_template('conteudos.html', imagens=imagens)

# Página de contato
COMENTARIOS_JSON = 'comentarios.json'

def salvar_comentario(nome, email, mensagem):
    comentarios = []
    if os.path.exists(COMENTARIOS_JSON):
        with open(COMENTARIOS_JSON, 'r', encoding='utf-8') as f:
            comentarios = json.load(f)
    comentarios.append({'nome': nome, 'email': email, 'mensagem': mensagem})
    with open(COMENTARIOS_JSON, 'w', encoding='utf-8') as f:
        json.dump(comentarios, f, ensure_ascii=False, indent=2)

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']
        salvar_comentario(nome, email, mensagem)
        return redirect(url_for('contato'))

    comentarios = []
    if os.path.exists(COMENTARIOS_JSON):
        with open(COMENTARIOS_JSON, 'r', encoding='utf-8') as f:
            comentarios = json.load(f)

    return render_template('contato.html', comentarios=comentarios)


# Função que salva título e descrição da imagem
def salvar_dados_imagem(nome_arquivo, titulo, descricao):
    dados = []
    if os.path.exists(DADOS_JSON):
        with open(DADOS_JSON, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    dados.append({'nome': nome_arquivo, 'titulo': titulo, 'descricao': descricao})
    with open(DADOS_JSON, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# Upload de imagem
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            salvar_dados_imagem(filename, titulo, descricao)
            return redirect(url_for('conteudos'))
    return render_template('upload.html')

# Execução
if __name__ == '__main__':
    app.run(debug=True)
