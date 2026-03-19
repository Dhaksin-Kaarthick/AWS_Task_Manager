import json
import boto3
import uuid
from boto3.dynamodb.conditions import Attr, Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TasksTable')


def lambda_handler(event, context):
    try:
        print("EVENT:", json.dumps(event))

        method = event.get('httpMethod', 'UNKNOWN')
        print("Method:", method)

        # 🔐 Get user from Cognito token (safe handling)
        authorizer = event.get('requestContext', {}).get('authorizer')

        if not authorizer:
            print("ERROR: No authorizer found")
            return response(401, "Unauthorized - no authorizer")

        claims = authorizer.get('claims') or authorizer.get('jwt', {}).get('claims')

        if not claims:
            print("ERROR: No claims found")
            return response(401, "Unauthorized - no claims")

        user = claims.get('sub')
        print("User:", user)

        # Parse body safely
        body = json.loads(event['body']) if event.get('body') else {}
        print("Body:", body)

        # ✅ CREATE
        if method == 'POST':
            if 'task' not in body:
                return response(400, "Task is required")

            task_id = str(uuid.uuid4())

            table.put_item(Item={
                'taskId': task_id,
                'task': body['task'],
                'taskOwner': user
            })

            return response(200, {"message": "Task added", "taskId": task_id})

        # ✅ READ (GSI QUERY - OPTIMIZED)
        elif method == 'GET':
            data = table.query(
                IndexName='taskOwner-index',
                KeyConditionExpression=Key('taskOwner').eq(user)
            )

            return response(200, data.get('Items', []))

        # ✅ UPDATE (ONLY OWNER)
        elif method == 'PUT':
            if 'taskId' not in body or 'task' not in body:
                return response(400, "taskId and task required")

            table.update_item(
                Key={'taskId': body['taskId']},
                UpdateExpression='SET task = :val',
                ConditionExpression=Attr('taskOwner').eq(user),
                ExpressionAttributeValues={
                    ':val': body['task']
                }
            )

            return response(200, {"message": "Task updated"})

        # ✅ DELETE (ONLY OWNER)
        elif method == 'DELETE':
            if 'taskId' not in body:
                return response(400, "taskId required")

            table.delete_item(
                Key={'taskId': body['taskId']},
                ConditionExpression=Attr('taskOwner').eq(user)
            )

            return response(200, {"message": "Task deleted"})

        else:
            return response(405, f"Method {method} not allowed")

    except Exception as e:
        print("ERROR:", str(e))  # 🔥 important for debugging
        return response(500, str(e))


def response(status, body):
    return {
        'statusCode': status,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps(body)
    }