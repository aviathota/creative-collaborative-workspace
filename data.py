import boto3
import db_secrets as sec

client = boto3.client('dynamodb', aws_access_key_id = sec.aws_access_key_id, aws_secret_access_key = sec.aws_secret_access_key, region_name = 'us-east-2')
tableName = "ccw-projects"

def createNewProject(name, user_id):
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
            print("Adding user " + user_id + " failed.")
            return "fail"
    return "success"