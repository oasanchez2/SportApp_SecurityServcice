from dataclasses import dataclass
from datetime import datetime

@dataclass
class RegisterModel:
    id_usuario: str   
    email: str
    password: str
    rol: str
 
@dataclass   
class RegisterJsonModel:
    id_usuario: str
    email: str
    password: str
    rol: str