from flask import Flask, jsonify, request, Blueprint
from ..commands.reset_notificacion import ResetNotificacion
from ..commands.login_usuario import LoginUsuario
from ..commands.register_usuario import RegisterUsuario
from ..commands.confirmar_registro_usuario import ConfirmarRegistroUsuario
from ..commands.desafio_mfa import DesafioMfa
from ..commands.verificar_mfa import VerifyMfa
from ..commands.get_user import GetUser
 
security_blueprint = Blueprint('security', __name__)

@security_blueprint.route('/security/login', methods = ['POST'])
def login():
    result = LoginUsuario(request.get_json()).execute()
    return jsonify(result), 201

@security_blueprint.route('/security/desafio-mfa', methods = ['POST'])
def activar_mfa():
    result = DesafioMfa(request.get_json()).execute()
    return jsonify(result)

@security_blueprint.route('/security/confirmar-registro', methods = ['POST'])
def confirmar_registro():
    result = ConfirmarRegistroUsuario(request.get_json()).execute()
    return jsonify(result), 201

@security_blueprint.route('/security/register', methods = ['POST'])
def register():
    user = RegisterUsuario(request.get_json()).execute()
    return jsonify(user), 201

@security_blueprint.route('/security/verify-mfa', methods = ['POST'])
def verify_mfa():
    user = VerifyMfa(request.get_json()).execute()
    return jsonify(user)

@security_blueprint.route('/security/me', methods = ['GET'])
def show():
    user = GetUser(auth_token()).execute()
    print(user)
    return jsonify(user)

@security_blueprint.route('/security/ping', methods = ['GET'])
def ping():
    return 'pong'

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization