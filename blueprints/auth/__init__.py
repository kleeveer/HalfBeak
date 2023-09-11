from functools import wraps

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from .forms import LoginForm, RegistrationForm
from db import MicroDB

from log import Log

from locales import load_lang

bp = Blueprint("auth", __name__, template_folder='templates/')

db = MicroDB('users_db', "./db/")

log = Log('auth', ['ip', 'tipo', 'status', 'alvo'])


def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'username' not in session:
      log.logger([
        request.remote_addr, 'movimento restrito', 'falhou', request.base_url
      ])
      return redirect(url_for('auth.login'))
    log.logger(
      [request.remote_addr, 'movimento restrito', 'sucesso', request.base_url])
    return f(*args, **kwargs)

  return decorated_function


@bp.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  bunk_of_string = load_lang(session.get('lang'),'pt_BR')
  if request.method == 'POST' and form.validate_on_submit():
    username = str(form.username.data)
    password = str(form.password.data)

    if not username.isdigit():
      log.logger([request.remote_addr, 'login', 'violado', username])
      return render_template('login.html',
                             form=form,
                             error="Apenas digitos no cpf",
                             bunk_of_string=bunk_of_string)

    if db.get(username) == None:
      log.logger([request.remote_addr, 'login', 'violado', username])
      return render_template('login.html',
                             form=form,
                             error='Usuário não existe',
                             bunk_of_string=bunk_of_string)

    if db.get(username).get("password") != password:
      log.logger([request.remote_addr, 'login', 'violado', username])
      return render_template('login.html',
                             form=form,
                             error='Credenciais erradas',
                             bunk_of_string=bunk_of_string)

    log.logger([request.remote_addr, 'login', 'sucesso', username])
    session['username'] = username
    return redirect(url_for('home'))

  log.logger([request.remote_addr, 'login', 'acesso', '---'])
  return render_template('login.html',
                         form=form,
                         languages={
                           1: "Entrar",
                           2: 'Digite Aqui'
                         })


@bp.route('/logout')
@login_required
def logout():
  log.logger([request.remote_addr, 'logout', 'acesso', '---'])
  username = str(session.get('username'))
  log.logger([request.remote_addr, 'logout', 'sucesso', username])
  session.pop('username', None)
  return redirect(url_for('auth.login'))


# Rota para a página de cadastro
@bp.route('/register', methods=['GET', 'POST'])
def register():
  bunk_of_string = load_lang(session.get('lang'),'pt_BR')
  # Gerar ID de funcionario
  form = RegistrationForm()
  if request.method == 'POST' and form.validate_on_submit():
    name = str(form.name.data)
    username = str(form.username.data)
    password = str(form.password.data)
    password2 = str(form.password2.data)

    if not username.isdigit():
      log.logger([request.remote_addr, 'signup', 'violado', username])
      return render_template('register.html',
                             form=form,
                             error="Apenas digitos no cpf",
                             bunk_of_string=bunk_of_string)

    if db.get(username) is not None:
      log.logger([request.remote_addr, 'signup', 'violado', username])
      return render_template('register.html',
                             form=form,
                             error="Usuário já existe",
                             bunk_of_string=bunk_of_string)

    if password != password2:
      log.logger([request.remote_addr, 'signup', 'violado', username])
      return render_template('register.html',
                             form=form,
                             error="As senhas não estão coesas",
                             bunk_of_string=bunk_of_string)

    log.logger([request.remote_addr, 'signup', 'sucesso', username])
    db.set(username, {"name": name, "password": password})
    db.save()

    return redirect(url_for('auth.login'))

  log.logger([request.remote_addr, 'signup', 'acesso', '---'])
  return render_template('register.html', form=form, bunk_of_string=bunk_of_string)
