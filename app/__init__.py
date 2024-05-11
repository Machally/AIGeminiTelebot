from flask import Flask
from dotenv import load_dotenv
from os import environ
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Access environment variables
bot_token = environ.get("bot_token")
bot_user_name = environ.get("bot_user_name")

from .dashboard import *
