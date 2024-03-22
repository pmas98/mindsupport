# utils.py
from rest_framework_simplejwt.models import TokenUser

def custom_jwt_payload_handler(user):
    payload = TokenUser.get_token_payload(user)
    payload['usuario_id'] = user.id
    return payload