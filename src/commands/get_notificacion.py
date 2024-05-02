from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, NotificacionNotFoundError
from ..dynamodb_notificacion import DynamoDbNotificacion

class GetNotificacion (BaseCommannd):
  def __init__(self, id_notificacion):
    if id_notificacion and id_notificacion.strip():
      self.id_notificacion = id_notificacion
    else:
      raise InvalidParams()
    
    self.db = DynamoDbNotificacion()
  
  def execute(self):
    
    result  = self.db.get_item(self.id_notificacion)
    if result is None:
      raise NotificacionNotFoundError()
    
    return result