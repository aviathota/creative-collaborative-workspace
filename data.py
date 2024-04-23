import boto3
import db_secrets as sec

client = boto3.client('dynamodb', aws_access_key_id = sec.aws_access_key_id, aws_secret_access_key = sec.aws_secret_access_key, region_name = 'us-east-2')
tableName = "ccw-projects"

item = {
    'ProjectID': {'S': 'hi'},
    'UserIDs': {'L': [{'N': 1}]}
}

response = client.put_item(
    TableName=tableName,
    Item=item
)

print("PutItem succeeded:")
print(response)