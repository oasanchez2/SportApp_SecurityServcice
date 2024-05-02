from .base_command import BaseCommannd
from ..dynamodb_notificacion import DynamoDbNotificacion

class ResetNotificacion(BaseCommannd):  
  def __init__(self):
    self.db = DynamoDbNotificacion()

  def execute(self):
    self.db.deleteTable()
    self.db.create_table()