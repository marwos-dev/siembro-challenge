from datetime import datetime, timezone
from typing import Annotated, Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.auth0 import Auth0Error, verify_jwt_token
from app.db.models.user import User
from app.db.session import get_db
from app.utils.random_generators import random_name, random_email
from random import randint



security = HTTPBearer(auto_error=False)


class CurrentUser:
    """
    Objeto de conveniencia para pasar tanto el modelo User
    como los claims del token.

    | Claim   | Qué significa            |
    | ------- | ------------------------ |
    | `sub`   | ID único del usuario     |
    | `email` | Email del usuario        |
    | `name`  | Nombre del usuario       |
    | `iat`   | Cuándo se creó el token  |
    | `exp`   | Cuándo expira            |
    | `iss`   | Quién lo emitió          |
    | `aud`   | Para qué API fue emitido |

    """

    def __init__(self, user: User, claims: Dict[str, Any]):
        self.user = user
        self.claims = claims


def get_token(
        credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )
    return credentials.credentials


def get_current_user(
        token: Annotated[str, Depends(get_token)],
        db: Annotated[Session, Depends(get_db)],
) -> CurrentUser:
    """
    - Verifica el token contra Auth0
    - Crea/actualiza el usuario según el sub
    - Devuelve CurrentUser(user, claims)
    """
    try:
        claims = verify_jwt_token(token)
    except Auth0Error as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    sub = claims.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing 'sub' claim",
        )

    email = random_email(randint(1, 1000))
    name = random_name()

    # Buscar usuario por auth0_sub
    user = db.query(User).filter(User.auth0_sub == sub).first()

    now = datetime.now(timezone.utc)

    if user is None:
        # Primera vez que entra con este sub
        user = User(
            auth0_sub=sub,
            email=email,
            name=name,
            created_at=now,
            metadata_json={"last_login_at": now.strftime("%Y-%m-%d %H:%M:%S")},
        )
        db.add(user)
    else:
        # Actualizar nombre/email si cambiaron, y last_login_at
        user.last_login_at = now
        if email and user.email != email:
            user.email = email
        if name and user.name != name:
            user.name = name

    db.commit()
    db.refresh(user)

    return CurrentUser(user=user, claims=claims)
