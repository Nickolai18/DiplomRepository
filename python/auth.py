from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(secret_key, algoritm, data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, secret_key, algorithm=algoritm)
    return encode_jwt

print(verify_password('1234', '$2b$12$G5DYKxHL6DMAVZwsRCWZIuO59N5Y6MrfSyRvCL67PeOKihjQvrhNa'))

