from flask import Flask, jsonify, request, Blueprint
from ..commands.create_notificacion import CreateNotificacion
from ..commands.get_notificacion import  GetNotificacion
from ..commands.get_notificacion_user import GetNotificacionUser
from ..commands.reset_notificacion import ResetNotificacion
from ..commands.LoginUsuario import LoginUsuario
 
security_blueprint = Blueprint('security', __name__)

@security_blueprint.route('/security/login', methods = ['POST'])
def login():
    notificacion = LoginUsuario(request.get_json()).execute()
    return jsonify(notificacion), 201

@security_blueprint.route('/security/ping', methods = ['GET'])
def ping():
    return 'pong'

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization