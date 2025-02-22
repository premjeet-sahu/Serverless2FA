import boto3
import os
import uuid
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

# Constants
TOKEN_TTL_SECONDS = 300  # Tokens expire after 5 minutes
DYNAMODB_TABLE = os.environ["DYNAMODB_TABLE"]

# Initialize AWS clients
dynamodb = boto3.client("dynamodb")

def generate_token():
    """Generates a random single-use token."""
    return str(uuid.uuid4()).replace("-", "")[:15]

def save_token(user_id, token):
    """Saves the token in DynamoDB."""
    expiry_time = int((datetime.utcnow() + timedelta(seconds=TOKEN_TTL_SECONDS)).timestamp())
    try:
        dynamodb.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                "user_id": {"S": user_id},
                "token": {"S": token},
                "expiry_time": {"N": str(expiry_time)}
            }
        )
    except ClientError as e:
        print(f"Error saving token: {e}")
        raise

def lambda_handler(event, context):
    """Lambda handler to generate and save 2FA tokens."""
    user_id = event["user_id"]

    # Generate a new token
    token = generate_token()

    # Save the token in the database
    save_token(user_id, token)

    return {
        "statusCode": 200,
        "body": "Token generated successfully. Token#: '" + token + "' expires in 5 minutes”
    }
