import boto3, os
from PIL import Image, ImageDraw

s3 = boto3.client('s3')
SRC_BUCKET = 'my-image-uploads-src-2026'
DEST_BUCKET = 'my-image-uploads-dest-2026'

def lambda_handler(event, context):
    key = event['key']
    download_path = f"/tmp/{os.path.basename(key)}"
    upload_path = f"/tmp/processed-{os.path.basename(key)}"
    
    # Download image from source bucket
    s3.download_file(SRC_BUCKET, key, download_path)
    
    # Process image with Pillow
    with Image.open(download_path) as img:
        img.thumbnail((800, 800))
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "WATERMARK", fill=(255, 255, 255))
        img.save(upload_path)
    
    # Upload to destination bucket
    dest_key = f"processed/{os.path.basename(key)}"
    s3.upload_file(upload_path, DEST_BUCKET, dest_key)
    
    return {'status': 'PROCESSED', 'key': key, 'destKey': dest_key}
