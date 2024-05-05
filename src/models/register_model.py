from dataclasses import dataclass
from datetime import datetime

@dataclass
class RegisterModel:
    id_usuario: str
    nombre: str
    apellido: str
    tipo_identificacion: str
    numero_identificacion: str
    genero_nacimiento: str
    edad: int
    peso: float
    estatura: float
    deportes_desea_practicar: str
    email: str
    password: str
    rol: str
 
@dataclass   
class RegisterJsonModel:
    id_usuario: str
    nombre: str
    apellido: str
    tipo_identificacion: str
    numero_identificacion: str
    genero_nacimiento: str
    edad: int
    peso: float
    estatura: float
    deportes_desea_practicar: str
    email: str
    password: str
    rol: str