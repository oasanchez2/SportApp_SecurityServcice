import uuid
from .base_command import BaseCommannd
from ..models.notificacion_model import NotificacionModel
from ..errors.errors import IncompleteParams, InvalidMessageError, SocioAlreadyExists
from ..dynamodb_notificacion import DynamoDbNotificacion
from datetime import datetime

class CreateNotificacion(BaseCommannd):
  
  def __init__(self, data):
    self.data = data
    self.db = DynamoDbNotificacion()
  
  def execute(self):
    try:

      posted_notificacion = NotificacionModel(str(uuid.uuid4()), self.data["id_usuario"], self.data["mensaje"],
                                       self.data["fecha_creado"] ,self.data["id_usuario_creo"], None)
      
      print(posted_notificacion)
      
      if not self.verificar_datos(self.data['mensaje']):
         raise InvalidMessageError
                  
      self.db.insert_item(posted_notificacion)
      
      return posted_notificacion
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
    
  def verificar_datos(self,mensaje):
    if mensaje and mensaje.strip():
        return True
    else:
        return False