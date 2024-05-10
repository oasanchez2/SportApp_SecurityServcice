from .base_command import BaseCommannd
from ..cognito_service import CognitoService
from botocore.exceptions import ClientError
from ..errors.errors import ExeptionCognitoCustomError,IncompleteParams
from ..models.register_model import RegisterModel,RegisterJsonModel

class ComfirmarRecuperarClave(BaseCommannd):
    def __init__(self, data):
        
            required_fields = ['email','confirmation_code','password']
            print(data)
            if not all(field in data for field in required_fields):
                raise IncompleteParams()
                    
            self.data = data
            self.cognito = CognitoService()
            
    def execute(self):
        try:
            print(self.data)    
            response = self.cognito.confirm_forgot_password(self.data['email'],self.data['confirmation_code'],self.data['password'])                       
            return response
        
        except ClientError as err: 
            print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
            http_code = err.response['ResponseMetadata']['HTTPStatusCode']
            message =  err.response['Error']['Code'] + '.' + err.response['Error']['Message']      
            raise ExeptionCognitoCustomError(http_code, message)
