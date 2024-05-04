import boto3
import hmac
import base64
import hashlib
import os
from botocore.exceptions import ClientError

class CognitoService:
    def __init__(self, cognito_client=None):
        if cognito_client is None:
            self.cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
        else:
            self.cognito_client = cognito_client
        
        self.CLIENT_ID = os.environ['APP_SPORTAPP']
    '''
    def create_user(self, username, password):
        self.cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=username,
            TemporaryPassword=password,
            MessageAction='SUPPRESS'
        )
        self.cognito_client.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=username,
            Password=password,
            Permanent=True
        )
    '''
    def sign_up(self, username, password, rol):
        response = self.cognito_client.sign_up(
                ClientId=self.CLIENT_ID,
                Username=username,
                Password=password,
                SecretHash= self.calculate_secret_hash(os.environ['APP_SPORTAPP'], os.environ['APP_SPORTAPPCLIENT'], username),
                UserAttributes=[
                    {
                        'Name': 'custom:rol',
                        'Value': rol
                    }
                ]
            )
        return response
    
    def initiate_auth(self, username, password):
        response = self.cognito_client.initiate_auth(            
            ClientId=self.CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': self.calculate_secret_hash(os.environ['APP_SPORTAPP'], os.environ['APP_SPORTAPPCLIENT'], username)
            }
        )
        return response
    
    def associate_software_token(self, access_token):
        response = self.cognito_client.associate_software_token(
            Session=access_token
        )
        return response
    
    def verify_software_token(self, access_token, user_code):
        response = self.cognito_client.verify_software_token(
            Session=access_token,
            UserCode=user_code
        )
        return response
    
    def calculate_secret_hash(self,client_id, client_secret, username):
        msg = username + client_id
        dig = hmac.new(str(client_secret).encode('utf-8'), 
                    msg=str(msg).encode('utf-8'), 
                    digestmod=hashlib.sha256).digest()
        return base64.b64encode(dig).decode()