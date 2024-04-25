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

def getProjectInfo(projectName):
    tableName = "ccw-projects"
    try:
        response = client.get_item(
            TableName=tableName,
            Key={'ProjectID': {'S': projectName}}
        )

        item = response.get('Item', {})
        
        project_info = {
            'name': item.get('ProjectID', {}).get('S', ''),
            'owner': item.get('Owner', {}).get('S', ''),
            'contributors': [contributor['S'] for contributor in item.get('Members', {}).get('L', [])]
        }

        return project_info
    except:
        return "fail"
    
def checkProjectPerms(user_id, project_id):
    tableName = "ccw-projects"
    try:
        response = client.query(
            TableName=tableName,
            KeyConditionExpression='ProjectID = :pid',
            FilterExpression='contains(Members, :uid)',
            ExpressionAttributeValues={
                ':pid': {'S': project_id},
                ':uid': {'S': user_id}
            }
        )
        if len(response['Items']) > 0:
            return "success"
        else:
            return "fail"    
    except Exception as e:
        return "fail"

def checkOwnerPerms(user_id, project_id):
    tableName = "ccw-projects"
    try:
        response = client.get_item(
            TableName=tableName,
            Key={
                'ProjectID': {'S': project_id}
            },
            ProjectionExpression='#o',
            ExpressionAttributeNames={'#o': 'Owner'}
        )
        owner = response.get('Item', {}).get('Owner', {}).get('S', '')

        if owner == user_id:
            return "success"
        else:
            return "fail"
    except:
        return "fail"

def createTask(project_id, task_name, assignees):
    tableName = "ccw-tasks"
    new_item = {
        'TaskID': {'S': str(random.getrandbits(128))},
        'ProjectID': {'S': project_id},
        'TaskName': {'S': task_name},
        'Assignees': {'L': [{'S': assignee} for assignee in assignees]}
    }
    try:
        response = client.put_item(
            TableName=tableName,
            Item=new_item
        )
        
        return "success"
    except:
        return "fail"

def purgeTasks(project_id):
    tableName = "ccw-tasks"
    try:
        response = client.scan(
            TableName=tableName,
            FilterExpression='ProjectID = :pid',
            ExpressionAttributeValues={':pid': {'S': project_id}}
        )

        for item in response['Items']:
            key = {'TaskID': item['TaskID']}
            client.delete_item(
                TableName=tableName,
                Key=key
            )
        return "success"
    except:
        return "fail"

def getTasks(project_id):
    tableName = "ccw-tasks"
    try:
        response = client.scan(
            TableName=tableName,
            FilterExpression='ProjectID = :pid',
            ExpressionAttributeValues={':pid': {'S': project_id}}
        )

        tasks = []
        for item in response['Items']:
            task = {
                'name': item.get('TaskName', {}).get('S', ''),
                'assignees': [assignee.get('S', '') for assignee in item.get('Assignees', {}).get('L', [])]
            }
            tasks.append(task)
        return tasks
    except:
        return "fail"

def getMyTasks(user_id):
    tableName = "ccw-tasks"
    try:
        response = client.scan(
            TableName=tableName,
            FilterExpression='contains(Assignees, :user)',
            ExpressionAttributeValues={':user': {'S': user_id}}
        )

        tasks = []
        for item in response.get('Items', []):
            task = {
                'project_id': item.get('ProjectID', {}).get('S', ''),
                'task_name': item.get('TaskName', {}).get('S', ''),
                'assignees': item.get('Assignees', {}).get('L', [])
            }
            tasks.append(task)

        return tasks
    except:
        return "fail"

def completeTask(task_name, project_id):
    tableName = "ccw-tasks"
    try:
        response = client.scan(
            TableName=tableName,
            FilterExpression='TaskName = :tname AND ProjectID = :pid',
            ExpressionAttributeValues={
                ':tname': {'S': task_name},
                ':pid': {'S': project_id}
            }
        )
        items = response['Items']
        
        for item in items:
            client.delete_item(
                TableName=tableName,
                Key={
                    'TaskID': item['TaskID']
                }
            )
        
        return "success"
    except Exception as e:
        return "fail"