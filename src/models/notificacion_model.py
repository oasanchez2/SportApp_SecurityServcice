from dataclasses import dataclass
from datetime import datetime


@dataclass
class NotificacionModel:
    id_notificacion: str
    id_usuario: str
    mensaje: str
    fecha_creado: datetime
    id_usuario_creo: str
    fecha_lectura: datetime = None
