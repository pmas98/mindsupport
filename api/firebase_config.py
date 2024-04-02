from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials
import dotenv
import os
import json

# Load environment variables from .env file
dotenv.load_dotenv()


class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"

    def ready(self):
        encoded_json = os.environ.get("FIREBASE_JSON")
        json_data = json.loads(encoded_json)
        cred = credentials.Certificate(json_data)

        firebase_admin.initialize_app(cred)
