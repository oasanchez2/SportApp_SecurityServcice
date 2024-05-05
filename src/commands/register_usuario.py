from .base_command import BaseCommannd
from ..cognito_service import CognitoService
from botocore.exceptions import ClientError
from ..errors.errors import Unauthorized, IncompleteParams, UserNotFoundError, UserNotConfirmedError, ClientExError, PasswordResetRequiredError, UserAlreadyExists, InvalidPasswordError, ClientInvalidParameterError
from ..models.register_model import RegisterModel,RegisterJsonModel

class RegisterUsuario(BaseCommannd):
    
    def __init__(self, data):
       
        required_fields = ['nombre', 'apellido', 'tipo_identificacion', 'numero_identificacion', 
                           'genero_nacimiento', 'edad', 'peso', 'estatura', 'deportes_desea_practicar',   
                           'email', 'password','rol']
        print(data)
        if not all(field in data for field in required_fields):
            raise IncompleteParams()
                
        self.data = data
        self.cognito = CognitoService()
    
    def execute(self):
      
        try:
            user = RegisterModel('', self.data['nombre'], self.data['apellido'], self.data['tipo_identificacion'],
                                 self.data['numero_identificacion'], self.data['genero_nacimiento'], self.data['edad'], self.data['peso'],
                                 self.data['estatura'], self.data['deportes_desea_practicar'], self.data['email'], self.data['password'],
                                 self.data['rol'])
            response = self.cognito.sign_up(self.data['email'], self.data['password'], self.data['rol'])
            user.id_usuario = response['UserSub']
            return user
        except ClientError as err: 
            print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
            if err.response['Error']['Code'] == 'UsernameExistsException':
                raise UserAlreadyExists
            elif err.response['Error']['Code'] == 'InvalidPasswordException':
                raise InvalidPasswordError
            elif err.response['Error']['Code'] == 'InvalidParameterException':
                raise ClientInvalidParameterError
            if err.response['Error']['Code'] == 'NotAuthorizedException':
                raise Unauthorized
            elif err.response['Error']['Code'] == 'UserNotFoundException':
                raise UserNotFoundError
            elif err.response['Error']['Code'] == 'UserNotConfirmedException':
                raise UserNotConfirmedError
            elif err.response['Error']['Code'] == 'InvalidParameterException':
                raise IncompleteParams
            elif err.response['Error']['Code'] == 'PasswordResetRequiredException':
                raise PasswordResetRequiredError
            else:
                raise ClientExError