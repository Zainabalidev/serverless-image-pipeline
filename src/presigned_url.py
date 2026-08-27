import json, boto3

s3 = boto3.client('s3')
BUCKET_NAME = 'my-image-uploads-src-2026'

def lambda_handler(event, context):
    filename = event.get('queryStringParameters', {}).get('filename', 'test-image.jpg')
    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': BUCKET_NAME, 'Key': filename, 'ContentType': 'image/jpeg'},
        ExpiresIn=300
    )
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'uploadUrl': presigned_url, 'key': filename})
    }
