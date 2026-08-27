import boto3, time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ImageMetadata')

def lambda_handler(event, context):
    key = event['key']
    dest_key = event['destKey']
    
    table.put_item(
        Item={
            'imageId': key,
            'destKey': dest_key,
            'timestamp': int(time.time()),
            'status': 'COMPLETED'
        }
    )
    return {'status': 'SUCCESS', 'imageId': key}
