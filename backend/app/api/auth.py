"""
Authentication API
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from datetime import datetime, timedelta
import jwt
import hashlib

from app.core.config import settings
from app.core.database import get_db
from app.schemas import Token, UserCreate, UserResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm="HS256")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db=Depends(get_db)
) -> dict:
    """Get current authenticated user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = await db.fetchrow("SELECT * FROM users WHERE email = $1", email)
    if not user:
        raise credentials_exception

    return dict(user)


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db=Depends(get_db)
):
    """Register a new user"""
    import uuid

    # Check if user already exists
    existing = await db.fetchrow("SELECT id FROM users WHERE email = $1", user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = uuid.uuid4()
    password_hash = hash_password(user_data.password)

    row = await db.fetchrow("""
        INSERT INTO users (id, email, name, password_hash, role)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, email, name, role
    """, user_id, user_data.email, user_data.name, password_hash, user_data.role)

    return UserResponse(**dict(row))


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db)
):
    """Login and get access token"""
    user = await db.fetchrow("SELECT * FROM users WHERE email = $1", form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password_hash = hash_password(form_data.password)
    if user["password_hash"] != password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user["email"], "user_id": str(user["id"])}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        name=current_user["name"],
        role=current_user["role"]
    )
