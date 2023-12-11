import random
import string

def generate_code():
    caracteres = string.ascii_letters + string.digits  # letras maiúsculas, minúsculas e dígitos
    return ''.join(random.choice(caracteres) for _ in range(10)).upper()