from . import bp

from flask import abort, render_template, send_file, request, session

import os

from blueprints import auth

from log import Log

from locales import load_lang


log = Log('logs',['ip','username','tipo','status','rota'])

BASE_DIR = './log/folder'

@bp.route('/', defaults={'req_path': ''})
@bp.route('/<path:req_path>')
@auth.login_required
def dir_listing(req_path):
    bunk_of_string = load_lang(session.get('lang'),'pt_BR')
    
    log.logger([request.remote_addr,session.get('username'),'listagem','acesso',request.base_url])
    
    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)
    
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        log.logger([request.remote_addr,session.get('username'),'movimentação invalida','falhou',request.base_url])
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        f = open(abs_path,'r')
        data = f.read()
        f.close()
        headers, logs = log.format_to_python(data)
        
        
        log.logger([request.remote_addr,session.get('username'),'leitura','sucesso (no-limited)',request.base_url])
        return render_template('file.html',headers=headers,logs=logs,bunk_of_string=bunk_of_string)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files,bunk_of_string=bunk_of_string)