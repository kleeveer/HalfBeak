from flask import (Blueprint, redirect, render_template, request, url_for,
                   session)

from blueprints import auth

from log import Log

from db import MicroDB

bp = Blueprint("product_manager", __name__, template_folder='templates/')

p_db = MicroDB('products_db', "./db/")

log = Log('product_manager', ['ip', 'username', 'tipo', 'status'])

from locales import load_lang


@bp.route('/register', methods=["POST", "GET"])
@auth.login_required
def register_product():
  bunk_of_string = load_lang(session.get('lang'),'pt_BR')
  if request.method == "POST":
    name = request.form.get("name")
    code = str(request.form.get("code"))
    category = request.form.get("category", 'None')
    price = request.form.get("price")
    amount = request.form.get("amount")
    p_db.set(code, {
      "name": name,
      "category": category,
      "price": price,
      "amount": amount
    })
    log.logger([
      request.remote_addr,
      session.get('username'), 'cadastro', 'sucesso (no-secure)'
    ])
    return redirect(url_for('product_manager.list_products'))
  log.logger(
    [request.remote_addr,
     session.get('username'), 'cadastro', 'acesso'])
  return render_template('register_product.html', bunk_of_string=bunk_of_string)


@bp.route('/list/item', methods=["POST", "GET"])
@auth.login_required
def list_products():
  bunk_of_string = load_lang(session.get('lang'),'pt_BR')
  log.logger(
    [request.remote_addr,
     session.get('username'), 'listagem', 'acesso'])
  datas = p_db.get_all()
  return render_template('list_products.html', datas=datas, bunk_of_string=bunk_of_string)


@bp.route('/edit/item/<id>', methods=["POST", "GET"])
@auth.login_required
def edit_product(id):
  bunk_of_string = load_lang(session.get('lang'),'pt_BR')
  if request.method == "POST":
    datas = p_db.get_all()

    name = request.form.get("name")
    code = request.form.get("code")
    category = request.form.get("category")
    price = request.form.get("price")
    amount = request.form.get("amount")

    if id in datas:
      p_db.set(id, {
        "name": name,
        "category": category,
        "price": price,
        "amount": amount
      })
    log.logger([
      request.remote_addr,
      session.get('username'), 'edição', 'sucesso (no-secure)'
    ])
    return redirect(url_for('product_manager.list_products'), bunk_of_string=bunk_of_string)
  log.logger(
    [request.remote_addr,
     session.get('username'), 'edição', 'acesso'])
  return render_template('edit_product.html',
                         data=p_db.get(id),
                         id=id,
                         bunk_of_string=bunk_of_string)
