from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        # Path to the JSON file downloaded from Firebase Console
        cred = credentials.Certificate("/home/pedro/Documents/uniforDesWeb/mindsupport/api/mindsupport-5da6e-firebase-adminsdk-jtayr-8d86846a2c.json")
        
        # Initialize Firebase Admin SDK
        firebase_admin.initialize_app(cred)
