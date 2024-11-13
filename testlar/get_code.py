import random
import string

def generate_secret_code():
    characters = string.ascii_letters + string.digits + '-'
    code = ''.join(random.choices(characters, k=13))
    return code
