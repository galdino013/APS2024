from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    session
)
from flask_sqlalchemy import SQLAlchemy
import app as login_user
import os
import re
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pesticides.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return redirect('/login', code=302)


@app.route('/login')
def login():
    username = session.get('name')
    level = session.get('level')

    if username and level:
        return redirect('/farmers', code=302)
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    file = request.files['file']
    filename = file.filename

    # Validação do tipo de arquivo
    if re.match(r'.*\.(png|tif|gif|tiff|jpg|jpeg)$', filename, re.IGNORECASE):
        image_path = os.path.join('database/uploaded', filename)

        # Verifica se o diretório existe, se não, cria
        if not os.path.exists('database/uploaded'):
            os.makedirs('database/uploaded')

        file.save(image_path)

        # Chama o login de autenticação de usuário com a imagem
        user = login_user.main(image_path)
        if user:
            session['name'] = user['name']
            session['level'] = user['level']
            return redirect('/farmers')
        else:
            flash('Impressão digital incorreta ou não autorizada!')
            return redirect('/login', code=302)
    else:
        flash('Formato de arquivo inválido! Envie uma imagem PNG, TIF, GIF ou JPG.')
        return redirect('/login', code=302)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('name', None)
    session.pop('level', None)

    return redirect('/login', code=302)


@app.route('/farmers/')
def farmers():
    username = session.get('name')
    level = session.get('level')

    if username and level:
        levels = [*range(1, level + 1)]
        levels_string = str(levels).replace('[','(').replace(']',')')

        results = db.engine.execute(f'SELECT * FROM farmers WHERE category in {levels_string}')
        return render_template('farmers.html', results=results, username=username, level=level)
    else:
        flash('Não autorizado!')
        return redirect('/login', code=302)


if __name__ == "__main__":
    app.secret_key = secrets.token_urlsafe(24)
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)


# Código baseado em "Fingerprint-Enhancement-Python"
# Autor: Utkarsh Deshmukh
# Licença: BSD 2-Clause (https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python/blob/master/LICENSE)
