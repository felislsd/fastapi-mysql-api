from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Post
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv() 



DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    username: str

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Sprawdzam czy user_id istnieje
    db_user = db.query(User).filter(User.id == post.user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Tworzę posta po walidacji
    db_post = Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=list[PostRead])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    results = []
    for post in posts:
        user = db.query(User).filter(User.id == post.user_id).first()
        results.append(PostRead(id=post.id, title=post.title, content=post.content, user_id=user.id, username=user.username))
    return results
