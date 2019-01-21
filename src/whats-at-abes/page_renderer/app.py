import json
import boto3
from site_renderer import SiteRenderer

s3_client = boto3.client('s3')

S3_BUCKET = 'whatsatabes.com'
FILENAME = 'index.html'

def lambda_handler(event, context):
    renderer = SiteRenderer()
    rendered_output = renderer.render()

    s3_client.put_object(
        ACL='public-read',
        ContentType='text/html',
        Body=rendered_output,
        Bucket=S3_BUCKET,
        Key=FILENAME)
