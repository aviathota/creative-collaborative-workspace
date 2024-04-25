import boto3
import db_secrets as sec
from datetime import datetime
import random

client = boto3.client('dynamodb', aws_access_key_id = sec.aws_access_key_id, aws_secret_access_key = sec.aws_secret_access_key, region_name = 'us-east-2')


userData = {
    'email': None,
}

def createNewProject(name, user_id):
    tableName = "ccw-projects"
    new_item = {
        'ProjectID': {'S': name},
        'Owner': {'S': user_id},
        'Members': {'L': [{'S': user_id}]}
    }
    
    try:
        response = client.put_item(
            TableName=tableName,
            Item=new_item
        )
        
        return "success"
    except:
        return "fail"

def inviteMember(project_id, user_id):
    tableName = "ccw-projects"
    try:
        response = client.get_item(
            TableName=tableName,
            Key={
                'ProjectID': {'S': project_id}
            }
        )
        
        user_list = response['Item']['Members']['L']
        user_list.append({'S': user_id})
        
        client.update_item(
            TableName=tableName,
            Key={
                'ProjectID': {'S': project_id}
            },
            UpdateExpression='SET Members = :val',
            ExpressionAttributeValues={
                ':val': {'L': user_list}
            }
        )

        return "success"
    except:
        return "fail"

def inviteMembers(project_id, user_ids):
    for user_id in user_ids:
        response = inviteMember(project_id, user_id)
        if response == "fail":
            return "fail"
    return "success"

def updateUser(email, name, age, location, birthday, summary):
    tableName = "ccw-user-data"
    try:
        response = client.update_item(
            TableName=tableName,
            Key={
                'UserID': {'S': email}
            },
            UpdateExpression='SET #n = :n, #a = :a, #l = :l, #b = :b, #s = :s',
            ExpressionAttributeNames={
                '#n': 'name',
                '#a': 'age',
                '#l': 'location',
                '#b': 'birthday',
                '#s': 'summary'
            },
            ExpressionAttributeValues={
                ':n': {'S': name},
                ':a': {'N': str(age)},
                ':l': {'S': location},
                ':b': {'S': birthday},
                ':s': {'S': summary}
            },
            ReturnValues='UPDATED_NEW'
        )
        
        return "success"
    except:
        return "fail"

def createUser(email):
    tableName = "ccw-user-data"
    new_item = {
        'UserID': {'S': email},
    }
    
    try:
        response = client.put_item(
            TableName=tableName,
            Item=new_item
        )
        
        return "success"
    except:
        return "fail"
    
def retrieveUserData(email):
    tableName = "ccw-user-data"
    try:
        response = client.get_item(
            TableName=tableName,
            Key={
                'UserID': {'S': email}
            }
        )
        item = response['Item']
        user_data = {
            'name': item.get('name', {'S': ''}).get('S', ''),
            'age': int(item.get('age', {'N': '0'}).get('N', '0')),
            'location': item.get('location', {'S': ''}).get('S', ''),
            'birthday': item.get('birthday', {'S': ''}).get('S', ''),
            'summary': item.get('summary', {'S': ''}).get('S', '')
        }
        return user_data
    except:
        return "fail"

def createMessage(sender, receiver, message):
    tableName = "ccw-messages"
    new_item = {
        'MessageID': {'S': str(random.getrandbits(128))},
        'SenderID': {'S': sender},
        'ReceiverID': {'S': receiver},
        'Message': {'S': message},
        'Timestamp': {'S': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
    }
    
    try:
        response = client.put_item(
            TableName=tableName,
            Item=new_item
        )
        
        return "success"
    except:
        return "fail"

def fetchMessages(email):
    tableName = "ccw-messages"
    try:
        response = client.scan(
            TableName=tableName,
            FilterExpression='ReceiverID = :email',
            ExpressionAttributeValues={':email': {'S': email}}
        )
        messages = []
        for item in response.get('Items', []):
            message = {
                'message': item.get('Message', {}).get('S', ''),
                'sender': item.get('SenderID', {}).get('S', ''),
                'timestamp': item.get('Timestamp', {}).get('S', '')
            }
            messages.append(message)
        return messages
    except:
        return "fail"

def getProjectsWithUser(user_id):
    tableName = "ccw-projects"
    try:
        response = client.scan(
            TableName=tableName,
            FilterExpression='contains(Members, :user)',
            ExpressionAttributeValues={':user': {'S': user_id}}
        )
        
        projects = []
        for item in response['Items']:
            project = {
                'name': item['ProjectID']['S'],
                'owner': item['Owner']['S'],
                'contributors': item['Members']['L']
            }
            projects.append(project)
        
        return projects
    except:
        return "fail"