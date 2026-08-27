def lambda_handler(event, context):
    # Extracts key from SQS event or manual test event
    key = event.get('key') or event['Records'][0]['s3']['object']['key']
    allowed_ext = ('.jpg', '.jpeg', '.png', '.webp')
    
    if not key.lower().endswith(allowed_ext):
        raise Exception(f"Invalid file extension for file: {key}")
        
    return {'status': 'VALIDATED', 'key': key}
