import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta

def base64_encode(data):
    """encode data to base64"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64_decode(data):
    """decode base64 data"""
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def create_jwt(payload, secret_key):
    """create JWT"""
    # create header
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    # encode header and payload
    encoded_header = base64_encode(json.dumps(header).encode('utf-8'))
    encoded_payload = base64_encode(json.dumps(payload).encode('utf-8'))

    # create signature
    signature = hmac.new(
        secret_key.encode('utf-8'), 
        (encoded_header + "." + encoded_payload).encode('utf-8'), 
        hashlib.sha256
    ).digest()
    encoded_signature = base64_encode(signature)

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

def verify_jwt(token, secret_key):
    """verify JWT"""
    # token should have 3 parts
    parts = token.split('.')
    if len(parts) != 3:
        return False

    encoded_header, encoded_payload, encoded_signature = parts
    # re-create signature
    signature = hmac.new(
        secret_key.encode('utf-8'), 
        (encoded_header + "." + encoded_payload).encode('utf-8'), 
        hashlib.sha256
    ).digest()
    decoded_signature = base64_encode(signature)

    # compare re-created signature with encoded signature
    return decoded_signature == encoded_signature

# example usage
payload = {
    "sub": "1234567890",
    "name": "John Doe",
    "iat": datetime.utcnow(),
    "exp": datetime.utcnow() + timedelta(hours=1) # set expiration to 1 hour
}

secret_key = "your_secret_key"

# create JWT
token = create_jwt(payload, secret_key)
print("JWT:", token)

# verify JWT
is_valid = verify_jwt(token, secret_key)
print("Is JWT valid?", is_valid)
