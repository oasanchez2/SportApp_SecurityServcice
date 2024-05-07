from .base_command import BaseCommannd
from ..cognito_service import CognitoService
from botocore.exceptions import ClientError
from ..errors.errors import Unauthorized, IncompleteParams, UserNotFoundError, UserNotConfirmedError, ClientExError, ExpiredCodeExceptionError,CodeInvalidForUserError
from ..models.register_model import RegisterModel,RegisterJsonModel

class DesafioMfa(BaseCommannd):
    def __init__(self, data):
        
            required_fields = ['email', 'session', 'mfa_code']
            print(data)
            if not all(field in data for field in required_fields):
                raise IncompleteParams()
                    
            self.data = data
            self.cognito = CognitoService()
    
    def execute(self):
        try:
            print(self.data)    
            response = self.cognito.admin_respond_to_auth_challenge(self.data['session'],self.data['email'], self.data['mfa_code'])             
            return response
        
        except ClientError as err: 
            print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
            if err.response['Error']['Code'] == 'NotAuthorizedException':
                raise Unauthorized
            elif err.response['Error']['Code'] == 'UserNotFoundException':
                raise UserNotFoundError
            elif err.response['Error']['Code'] == 'UserNotConfirmedException':
                raise UserNotConfirmedError
            elif err.response['Error']['Code'] == 'InvalidParameterException':
                raise IncompleteParams
            elif err.response['Error']['Code'] == 'ExpiredCodeException':
                raise ExpiredCodeExceptionError
            elif err.response['Error']['Code'] == 'CodeMismatchException':
                raise CodeInvalidForUserError   
            else:
                raise ClientExError