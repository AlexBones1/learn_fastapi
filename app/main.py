import datetime

import uvicorn
import jwt
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

title = 'My first App'
SECRET_KEY = 'secret'
ALGORITHM = "HS256"

app = FastAPI(title=title)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    password: str


expiration_delta_minutes = 2  # Токен действителен в течение 2 минут
algorithm = 'HS256'  # Алгоритм шифрования
issue_datetime = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_delta_minutes)


def check_user(user: User):
    if "user" in user.username.lower() or "password" in user.password.lower():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return True


def get_user(user: User):
    if check_user(user):
        return User(username=user.username, password=user.password)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_dict = payload.get("sub")
        return User(username=user_dict.get("username"), password=user_dict.get("password"))
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


@app.post("/login")
def check_login(user: User):
    if check_user(user):
        return {
            "token": jwt.encode(
                {
                    "sub": {"username": user.username, "password": user.password},
                    "exp": issue_datetime,
                    "iat": datetime.datetime.utcnow()
                },
                SECRET_KEY,
                ALGORITHM
            )
        }


@app.get("/protected_resource")
def check_success(data_for_check: User | None = Depends(get_user_from_token)):
    if data_for_check:
        if get_user(data_for_check):
            return {"message": "Success"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8080, reload=True, workers=3)
