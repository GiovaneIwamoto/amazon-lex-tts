import hashlib

def generate_id(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()
