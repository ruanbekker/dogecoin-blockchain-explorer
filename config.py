import os

class Config:
    SECRET_KEY = "your-secret-key"
    DEBUG = True
    RPC_URL = os.environ['RPC_ENDPOINT']
    RPC_HEADERS = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": os.environ['RPC_API_KEY']
    }

