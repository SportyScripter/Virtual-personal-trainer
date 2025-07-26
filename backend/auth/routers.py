from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from jose import jwt

from auth.schemas import (
    UserCreate,
    RequestDetails,
    TokenSchama,
    ChangePassword,
)
from db.session import get_db
from auth.utils import (
    get_hashed_password,
    verify_password,
    create_access_token,
    get_user,
    create_refresh_token,
    get_current_active_user,
)
from models.user import User
from models.token import Token
from models.role import Role
from auth.auth_bearer import JWTBearer
from auth.utils import JWT_SECRET_KEY, ALGORITHM

user_router = APIRouter(prefix="/auth", tags=["auth"])


def check_is_correct_string(string: str):
    table_with_not_correct_characters = [
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "-",
        "_",
        "+",
        "=",
        "{",
        "}",
        "[",
        "]",
        "|",
        "\\",
        ":",
        ";",
        "'",
        '"',
        "<",
        ">",
        ",",
        ".",
        "?",
        "/",
        " ",
    ]
    if any(char in table_with_not_correct_characters for char in string):
        return False
    elif string.isnumeric():
        return False
    return True


def password_is_correct(password: str):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    table_with_correct_characters = [
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "-",
        "_",
        "+",
        "=",
        "{",
        "}",
        "[",
        "]",
        "|",
        "\\",
        ":",
        ";",
        "'",
        '"',
        "<",
        ">",
        ",",
        ".",
        "?",
        "/",
    ]
    return (
        True
        if all(char not in table_with_correct_characters for char in password)
        else False
    )


def get_token_response(user_id: int, db: Session):
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)

    token_db = Token(
        user_id=user_id,
        access_token=access_token,
        refresh_token=refresh_token,
        status=True,
    )
    db.add(token_db)
    try:
        db.commit()
    except Exception as e:
        print(f"Błąd podczas commit: {e}")
        raise
    db.refresh(token_db)

    return {"access_token": access_token, "refresh_token": refresh_token}


@user_router.post("/register", response_model=TokenSchama)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        if db.query(User).filter_by(email=user.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        if db.query(User).filter_by(username=user.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        if not check_is_correct_string(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username contains not correct characters",
            )
        if not check_is_correct_string(user.first_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="First name contains not correct characters",
            )
        if not check_is_correct_string(user.last_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Last name contains not correct characters",
            )
        if not password_is_correct(user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, and one digit",
            )
        encrypted_password = get_hashed_password(user.password)
        new_user = User(**user.dict())
        new_user.hashed_password = encrypted_password
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )
    return get_token_response(new_user.id, db)


@user_router.post("/login", response_model=TokenSchama)
async def login(request: RequestDetails, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    user.is_active = True
    hashed_pass = user.hashed_password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return get_token_response(user.id, db)


@user_router.post("/change_password")
async def change_password(request: RequestDetails, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    hashed_pass = user.hashed_password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    user.hashed_password = get_hashed_password(request.new_password)
    db.commit()
    db.refresh(user)
    return {"message": "Password changed successfully"}


@user_router.post("/logout")
async def logout(dependecies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    try:
        token = dependecies
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_records = db.query(Token).filter(Token.user_id == user_id).all()
        user = db.query(User).filter(User.id == user_id).first()
        user.is_active = False
        for token_record in token_records:
            db.delete(token_record)
        db.commit()
        return {"message": "Logout successful"}
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Token expired") from e
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=403, detail="Invalid token") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@user_router.get("/users/me")
async def read_current_user_data(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@user_router.delete("/delete")
async def delete_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user_token = db.query(Token).filter(Token.user_id == user.id).all()
    for token in user_token:
        db.delete(token)
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
