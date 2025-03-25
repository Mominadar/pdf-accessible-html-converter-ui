from utils.helpers import get_current_date_str
from utils.logger import Logger
import boto3
import os
from dotenv import load_dotenv
from boto3.dynamodb.types import TypeDeserializer

load_dotenv()

logger = Logger(name="NLLB Logger")
logger = Logger.get_logger()

TABLE_NAME = os.environ["TABLE_NAME"]
TABLE_REGION = os.environ["TABLE_REGION"]

class DynamoDBClient():
    def __init__(self) -> None:
        self.client = boto3.client(service_name='dynamodb', region_name=TABLE_REGION)
        self.table = TABLE_NAME

    def find_all(self):
        try:
            data = self.client.scan(TableName=TABLE_NAME) 
            logger.info("Got data:")
            return data
        except Exception as e:
            logger.exception(
                "error '%s'.", e
            )
            raise
    
    def find_by_id(self, key_value):
        try:
            data = self.client.get_item(
                TableName=TABLE_NAME,
                Key={f'object_key': {'S': str(key_value)}}
            )
            deserializer = TypeDeserializer()
            python_dict = {k: deserializer.deserialize(v) for k,v in data["Item"].items()}

            return python_dict
        except Exception as e:
            logger.error(f'DB Exception: {str(e)}')
            raise
    
    def delete(self, key_value):
        try:
            data = self.client.delete_item(
                TableName=TABLE_NAME,
                Key={f'object_key': {'S': str(key_value)}}
            )
            return data
        except Exception as e:
            logger.error(f'DB Exception: {str(e)}')
            raise

    def find(self, key_name, key_value):
        try:
            expression_attribute_values= {
                ':user': {'S': key_value}
            }
            data = self.client.scan(TableName=TABLE_NAME,
                    FilterExpression=f'{key_name} = :user',
                    ExpressionAttributeValues=expression_attribute_values)
            d = []
            deserializer = TypeDeserializer()
            for item in data["Items"]:
                d.append({k: deserializer.deserialize(v) for k,v in item.items()})
            return d
        except Exception as e:
            logger.error(
                f"DB Exception {str(e)}"
            )
            raise

    def create(self, item):
        try:
            self.client.put_item(
                TableName=TABLE_NAME,
                Item=item
            )
        except Exception as e:
            logger.error(
                f"DB Exception {str(e)}"
            )
            raise
    
    def put(self, key, key_name, key_value):
        try:
            # Define the primary key of the item to update
            primary_key = {
                'object_key': {'S': key},
            }

            # Define the attributes to update
            update_expression = f"SET {key_name} = :val1, last_modified_at = :val2"
            expression_attribute_values = {
                ':val1': {'S': key_value},
                ':val2': {'S': get_current_date_str()}
            }

            # Update the item with the new values
            response = self.client.update_item(
                TableName=TABLE_NAME,
                Key=primary_key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW"
            )
            return response
        except Exception as e:
            logger.error(
                f"DB Exception {str(e)}"
            )
            raise