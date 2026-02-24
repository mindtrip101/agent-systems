import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .config import settings

security = HTTPBearer(auto_error=False)

def get_subject_and_scopes(creds: HTTPAuthorizationCredentials = Depends(security)):
    if not creds:
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = creds.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
            options={"require": ["sub", "aud", "iss"]},
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    sub = payload.get("sub")
    scopes = payload.get("scopes", [])
    if not isinstance(scopes, list):
        scopes = []
    return sub, set(scopes)
