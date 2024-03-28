from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.models import URL, User
from schemas.schemas import URLCreate, URLDisplay, UserCreate
from db.database import SessionLocal, engine
from models.models import Base
from core.utils import generate_short_url
from starlette.responses import RedirectResponse
from core.security import verify_password, create_access_token
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from datetime import timedelta
from jose import JWTError, jwt
from urllib.parse import urlparse
from typing import List

router = APIRouter()

Base.metadata.create_all(bind=engine)  # Creates the database tables

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user 

@router.post("/urls/", response_model=URLDisplay)
def create_short_url(url_create: URLCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Use the generate_short_url function to create a unique short URL identifier
    short_url = generate_short_url()
    db_url = URL(owner_id=current_user.id, original_url=url_create.original_url, short_url=short_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

@router.get("/{short_url}")
def redirect_to_original(short_url: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_url == short_url).first()
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Increment click_count
    url.click_count += 1
    db.commit()  # Make sure to commit the changes

    # Ensure the URL includes a scheme
    parsed_url = urlparse(url.original_url)
    if not parsed_url.scheme:
        redirect_url = "http://" + url.original_url
    else:
        redirect_url = url.original_url

    return RedirectResponse(redirect_url)


@router.get("/myurls/", response_model=List[URLDisplay])
def read_user_urls(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_urls = db.query(URL).filter(URL.owner_id == current_user.id).all()
    return user_urls
