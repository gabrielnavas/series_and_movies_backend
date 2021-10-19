import jwt
import datetime
from typing import Dict, Any, Mapping


class JwtCrypter:
    __secret_token = "iamasecrettoken"
    __algorithm = "HS256"
    __time_expiration = datetime.timedelta(days=1)

    def create(self, payload: Mapping[str, Any]) -> str:
        payload["exp"] = datetime.datetime.utcnow() + self.__time_expiration
        return jwt.encode(payload, self.__secret_token, algorithm=self.__algorithm)

    def decode(self, encoded_jwt: str) -> Dict[str, Any]:
        return jwt.decode(encoded_jwt, self.__secret_token, algorithms=[self.__algorithm])
