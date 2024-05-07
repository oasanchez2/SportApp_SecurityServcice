from .base_command import BaseCommannd
from ..cognito_service import CognitoService
from botocore.exceptions import ClientError
from ..errors.errors import Unauthorized, IncompleteParams, UserNotFoundError, UserNotConfirmedError, ClientExError, PasswordResetRequiredError, ClientInvalidParameterError

class LoginUsuario(BaseCommannd):

    def __init__(self, data):
       
        if 'username' not in data or 'password' not in data:
            raise IncompleteParams()
        
        self.data = data
        self.cognito = CognitoService()

    def execute(self):
      
        try:
            response = self.cognito.initiate_auth(self.data['username'], self.data['password'])
            print(response)
            challenge_name = response.get("ChallengeName", None)
            if challenge_name == "MFA_SETUP":
                if (
                "SOFTWARE_TOKEN_MFA"
                in response["ChallengeParameters"]["MFAS_CAN_SETUP"]
                ):
                    response_associate = self.cognito.associate_software_token(response["Session"])
                    response_associate.pop("ResponseMetadata", None)
                    response.update(response_associate)
                    pass
                else:
                    raise RuntimeError(
                        "The user pool requires MFA setup, but the user pool is not "
                        "configured for TOTP MFA."
                    )
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
            elif err.response['Error']['Code'] == 'PasswordResetRequiredException':
                raise PasswordResetRequiredError
            else:
                raise ClientExError