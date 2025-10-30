from passlib.context import CryptContext
import os

pwd_context = CryptContext(
    schemes=["argon2"]  
)

PEPPER = os.environ.get('PEPPER')

print(f'PEPPER: {PEPPER}')

def _apply_pepper(password: str):
    return password + (PEPPER or "")

def hash_password(password: str):
    return pwd_context.hash(_apply_pepper(password))

def verify_password(password: str, hashed: str):
    return pwd_context.verify(_apply_pepper(password), hashed)

def needs_rehash(hashed):
    return pwd_context.needs_update(hashed)