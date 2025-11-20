# app/auth/auth0.py
from functools import lru_cache
from typing import Any, Dict

import certifi
import httpx
from jose import jwt
from jose.exceptions import JWTError

from app.core.settings import settings


class Auth0Error(Exception):
    ...


@lru_cache(maxsize=1)
def get_jwks() -> Dict[str, Any]:
    """
    Descarga y cachea el JWKS de Auth0.
    Se cachea en memoria gracias a lru_cache.
    """
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    resp = httpx.get(jwks_url, timeout=5.0, verify=certifi.where())
    resp.raise_for_status()
    return resp.json()


def verify_jwt_token(token: str) -> Dict[str, Any]:
    # 1) Leer header sin validar
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise Auth0Error("Invalid JWT header") from exc

    # 2) Verificar que tenga kid
    if "kid" not in unverified_header:
        raise Auth0Error("Invalid token header: 'kid' missing")

    # 3) Obtener el JWKS y buscar la clave que matchea el kid
    jwks = get_jwks()
    keys = jwks.get("keys", [])

    rsa_key: Dict[str, Any] = {}
    for key in keys:
        if key.get("kid") == unverified_header["kid"]:
            rsa_key = {
                "kty": key.get("kty"),
                "kid": key.get("kid"),
                "use": key.get("use"),
                "n": key.get("n"),
                "e": key.get("e"),
            }
            break

    if not rsa_key:
        raise Auth0Error("no se encontraron las claves apropiadas")

    # 4) Decodificar y validar el token con esa clave
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=[settings.AUTH0_ALGORITHMS],
            audience=settings.AUTH0_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
        )
        return payload
    except JWTError as exc:
        raise Auth0Error("Invalid token") from exc
