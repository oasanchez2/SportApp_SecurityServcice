from .base_command import BaseCommannd
from ..cognito_service import CognitoService
from botocore.exceptions import ClientError
from ..errors.errors import ExeptionCognitoCustomError,IncompleteParams

class RecuperarClave(BaseCommannd):
    def __init__(self, data):
        
            required_fields = ['email']
            print(data)
            if not all(field in data for field in required_fields):
                raise IncompleteParams()
                    
            self.data = data
            self.cognito = CognitoService()
            
    def execute(self):
        try:
            print(self.data)    
            response = self.cognito.forgot_password(self.data['email'])                       
            return response
        
        except ClientError as err: 
            print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
            http_code = err.response['ResponseMetadata']['HTTPStatusCode']
            message =  err.response['Error']['Code'] + '.' + err.response['Error']['Message']      
            raise ExeptionCognitoCustomError(http_code, message)
