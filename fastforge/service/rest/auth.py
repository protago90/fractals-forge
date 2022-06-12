from datetime import datetime, timedelta
from fastapi import HTTPException, status
from typing import Dict, NoReturn
from jose import jwt, JWTError
from passlib.context import CryptContext


CRYPTO_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')


class AuthCtrl():
    cipher: CryptContext = CRYPTO_CONTEXT

    def __init__(self, exp_time: int, hasher: str, secret: str) -> None:
        self.exp_time = exp_time
        self.hasher = hasher
        self.secret = secret

    def encrypt(self, msg: str) -> str:
        return self.cipher.hash(msg)

    def assert_crypto(self, msg: str, msg_hash: str) -> None:
        if not self.cipher.verify(msg, msg_hash):
            self.raise_auth_exc('Failed auth: false password.')

    def make_token_from_payload(self, data: dict, ttl: timedelta | None = None) -> str:
        ttl = ttl if ttl else timedelta(minutes=self.exp_time)
        data.update({'exp': datetime.utcnow() + ttl})
        try:
            return jwt.encode(data, self.secret, algorithm=self.hasher)
        except JWTError:
            self.raise_auth_exc('Failed auth: uncoded token.')

    def get_payload_from_token(self, stream: str) -> Dict:
        try:
            return jwt.decode(stream, self.secret, algorithms=[self.hasher])
        except jwt.ExpiredSignatureError:
            self.raise_auth_exc('Failed auth: expired token.')
        except JWTError:
            self.raise_auth_exc('Failed auth: invalid token.')                        

    @staticmethod
    def raise_auth_exc(msg: str) -> NoReturn:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail=msg, headers={'WWW-Authenticate': 'Bearer'},
        )
