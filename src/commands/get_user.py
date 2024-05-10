from .base_command import BaseCommannd
from ..errors.errors import ExeptionCognitoCustomError, IncompleteParams
from botocore.exceptions import ClientError
from ..cognito_service import CognitoService

class GetUser(BaseCommannd):
    def __init__(self, token = None):
        if token == None or token == "":
            raise IncompleteParams()
        else:
            self.token = self.parse_token(token)
            self.cognito = CognitoService()       
            
    
    def execute(self):
        try:
            response = self.cognito.get_user(self.token)
            print(response)
            
            return response
        except ClientError as err:
            print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
            http_code = err.response['ResponseMetadata']['HTTPStatusCode']
            message =  err.response['Error']['Code'] + '.' + err.response['Error']['Message']      
            raise ExeptionCognitoCustomError(http_code, message)
            
    
    def parse_token(self, token):
        return token.split(' ')[1]