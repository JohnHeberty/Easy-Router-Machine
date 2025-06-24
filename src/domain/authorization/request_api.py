from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.infra.config.api_config import login
import secrets

def verify_request(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    correct_username = secrets.compare_digest(credentials.username, login["User"])
    correct_password = secrets.compare_digest(credentials.password, login["Pass"])
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Dados de acesso incorretos!",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username