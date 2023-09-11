import os

from flask import Flask, redirect, render_template, session, url_for, request

from blueprints import auth, logs, product_manager
from db import MicroDB
from log import Log

from locales import load_lang, current_languages


# Configurações
app = Flask(__name__)
app.config['SECRET_KEY'] = "1#221z634SSa56s7e%8bA904"  # os.urandom(24)


# Inicialização do banco de dados de usuário temporaria
u_db = MicroDB('users_db', "./db/")

# Inicialização de sistema registros
log = Log('system', ['tipo', 'status', 'output'])

# Rota para a página inicial
@app.route('/')
@auth.login_required
def home():
  bunk_of_string = load_lang(session.get('lang'),'pt_BR')
  
  name = u_db.get(str(session.get('username'))).get('name')
  return render_template('home.html', name=name, bunk_of_string=bunk_of_string)


# Rota para fazer uma queima de arquivos
@app.route('/dump')
@auth.login_required
def dump_and_reset():
  log_folder = './log/folder'
  for arquivo in os.listdir(log_folder):
    caminho_completo = os.path.join(log_folder, arquivo)
    if os.path.isfile(caminho_completo):
      os.remove(caminho_completo)
  return redirect(url_for('home'))


# Rota para a página inicial
@app.route('/')
@auth.login_required
def config():
  bunk_of_string = load_lang(session.get('lang'),'pt_BR')
  
  name = u_db.get(str(session.get('username'))).get('name')
  return render_template('home.html', name=name, bunk_of_string=bunk_of_string)


@app.route('/set/lang/<lang>')
def set_lang(lang):
  if lang in current_languages:
    session['lang'] = lang
  else:
    session['lang'] = 'pt_BR'
    
  return redirect(url_for('config'))


if __name__ == '__main__':
  # Registro de blueprints
  try:
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(product_manager.bp, url_prefix='/product')
    app.register_blueprint(logs.bp, url_prefix='/log')
  except Exception as e:
    log.logger(['configurando', 'falhou', f'falhou a carregar blue prints: {e}'])

  try:
    log.logger(['iniciando', 'sucesso', 'o sistema foi iniciado'])
    app.run(host='0.0.0.0', port=5000, debug=True)
  except Exception as e:
    log.logger(['iniciando', 'falhou', f'o sistema falhou a iniciar iniciado: {e}'])
