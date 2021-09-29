import os
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_fernet(passwd:str, force:bool):
    passwd = passwd.encode("utf-8")
    key_file_name = "./secret/"+hashlib.md5(passwd).hexdigest()+hashlib.sha512(passwd).hexdigest()
    if os.path.isfile(key_file_name):
        f= open(key_file_name, 'rb')
        key = f.read()
        f.close()
    else:
        if force:
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(passwd))
            f= open(key_file_name, 'wb')
            f.write(key)
            f.close()
        else:
            return False
    f = Fernet(key)
    return f

def encrypt(data:str, password:str):
    encoded_data = data.encode()
    f = get_fernet(password, True)
    if f==False:
        return "ERROR"
    return f.encrypt(encoded_data)

def decrypt(data:str, password:str):
    encoded_data = data.encode()
    f = get_fernet(password, False)
    if f==False:
        return "ERROR"
    return f.decrypt(encoded_data).decode()
