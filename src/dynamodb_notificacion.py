import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
from .models.notificacion_model import NotificacionModel
from botocore.exceptions import ClientError

class DynamoDbInterface:
    def create_table(self):
        raise NotImplementedError
    
    def insert_item(self,notificacion: NotificacionModel):
        raise NotImplementedError
    
    def get_item(self,id_notificacion):
        raise NotImplementedError
  
    def tablaExits(self,name):
        raise NotImplementedError
    
    def deleteTable(self):
        raise NotImplementedError    
       

class DynamoDbNotificacion(DynamoDbInterface):
    def __init__(self,dynamodb=None):        
        # Crear una instancia de cliente DynamoDB
        if dynamodb is None:
            self.dynamodb = boto3.client('dynamodb',
                                    region_name='us-east-1',
                                    aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
                                    aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'])
        else:
            self.dynamodb = dynamodb

        self.table_name = 'notificaciones'

    # Funciones para interactuar con DynamoDB
    def create_table(self):
        if not self.tablaExits(self.table_name):

            self.dynamodb.create_table(
                    TableName=self.table_name,
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id_notificacion',
                            'AttributeType': 'S',
                        }
                    ],
                    KeySchema=[
                        {
                            'AttributeName': 'id_notificacion',
                            'KeyType': 'HASH'  # Clave de partición
                        }
                    ],        
                    BillingMode='PAY_PER_REQUEST'
                )
            
            # Espera hasta que la tabla exista
            self.dynamodb.get_waiter('table_exists').wait(TableName=self.table_name)
            print(f'Tabla {self.table_name} creada correctamente.')
        else:
            print(f"La tabla '{self.table_name}' ya existe.")

    def insert_item(self,notificacion: NotificacionModel):
        item = {
            "id_notificacion": {'S': notificacion.id_notificacion },
            'id_usuario': {'S': notificacion.id_usuario },
            'mensaje': {'S': notificacion.mensaje },
            'fecha_creado': {'S': str(notificacion.fecha_creado) },  # Datetime conversion
            'id_usuario_creo': {'S': notificacion.id_usuario_creo }                         
            # Puedes agregar más atributos según la definición de tu tabla
        }

        if notificacion.fecha_lectura is not None:
            item['fecha_lectura'] = {'S': str(notificacion.fecha_lectura)}
        else:
            item['fecha_lectura'] = {'S': '' }
        
        
        result = self.dynamodb.put_item(
            TableName=self.table_name,
            Item=item,
            ReturnConsumedCapacity='TOTAL'
        )

        print('Ítem insertado correctamente.')

    def get_item(self,id_notificacion):
        key = {
            'id_notificacion': {'S': id_notificacion }  # Clave de búsqueda
        }
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key=key
        )
        item = response.get('Item')
        if not item:
            return None
        
        # Extrae los valores de cada campo
        id_notificacion = item['id_notificacion']['S']
        id_usuario = item['id_usuario']['S']
        mensaje = item['mensaje']['S']
        fecha_creado = item['fecha_creado']['S']
        id_usuario_creo = item['id_usuario_creo']['S']
        fecha_lectura = item['fecha_lectura']['S']
        
        # Crea una instancia de la clase Entrenamiento
        notificacion = NotificacionModel(id_notificacion,id_usuario,mensaje,fecha_creado,id_usuario_creo,fecha_lectura)

        return notificacion
    
    def get_notificaciones_usuario(self,id_usuario):

         # Parámetros para la operación de escaneo
        parametros = {
            'TableName': self.table_name,
            'FilterExpression': '#id_usuario = :id_usuario',
            'ExpressionAttributeNames': {
                '#id_usuario': 'id_usuario'
            },
            'ExpressionAttributeValues': {
                ':id_usuario': {'S': id_usuario}
            }
        }

         # Realizar el escaneo
        response = self.dynamodb.scan(**parametros)
        print(response)
        # Obtener los items encontrados
        items = response.get('Items', [])
        
        # Procesar los items encontrados
        resultados = []
        for item in items:
            id_notificacion = item['id_notificacion']['S']
            id_usuario = item['id_usuario']['S']
            mensaje = item['mensaje']['S']
            fecha_creado = item['fecha_creado']['S']
            id_usuario_creo = item['id_usuario_creo']['S']
            fecha_lectura = item['fecha_lectura']['S']
        
            # Crea una instancia de la clase Entrenamiento
            notificacion = NotificacionModel(id_notificacion,id_usuario,mensaje,fecha_creado,id_usuario_creo,fecha_lectura)
            resultados.append(notificacion)
        
        return resultados
    
    def tablaExits(self,name):
        try:
            response = self.dynamodb.describe_table(TableName=name)
            print(response)
            return True
        except ClientError as err:
            print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                return False

    def deleteTable(self):
        # Eliminar la tabla
        self.dynamodb.delete_table(TableName=self.table_name)

        # Esperar hasta que la tabla no exista
        self.dynamodb.get_waiter('table_not_exists').wait(TableName=self.table_name)