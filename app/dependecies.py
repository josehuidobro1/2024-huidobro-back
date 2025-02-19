from fastapi import Depends, HTTPException, Header
from .auth import verify_token


async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401, detail="Missing Authorization Header")

    # Extraer el token del encabezado
    token = authorization.split("Bearer ")[-1]
    decoded_token = verify_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return decoded_token  # Retorna el usuario decodificado
