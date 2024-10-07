import os
from serverless_wsgi import handle_request
from trainomart_backend.wsgi import application

# Ensure the Django settings module is set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trainomart_backend.settings')

def handler(request, context):
    return {
        "statusCode": 200,
        "body": "Hello from Django on Vercel!"
    }
