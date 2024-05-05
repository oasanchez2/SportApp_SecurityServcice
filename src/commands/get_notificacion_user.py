from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, NotificacionNotFoundError
from ..dynamodb_notificacion import DynamoDbNotificacion

class GetNotificacionUser (BaseCommannd):
  def __init__(self, id_user):
    if id_user and id_user.strip():
      self.id_user = id_user
    else:
      raise InvalidParams()
    
    self.db = DynamoDbNotificacion()
  
  def execute(self):
    
    result  = self.db.get_notificaciones_usuario(self.id_user)
        
    return result