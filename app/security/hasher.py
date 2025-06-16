import bcrypt
from typing import Union

def hash_password(password: str) -> str:
    """Хеширует пароль с использованием bcrypt"""
    if not password:
        raise ValueError("Password cannot be empty")
    
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)  
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Проверяет пароль против хеша"""
    if not password or not hashed_password:
        return False
    
    try:
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Проверка формата хеша перед проверкой
        if not (hashed_password.startswith('$2a$') or hashed_password.startswith('$2b$')):
            return False
            
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except (ValueError, UnicodeError):
        return False