from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users' 

    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String(50), unique=True, nullable=False)  
    email = Column(String(120), unique=True, nullable=False)  
    password = Column(String(100), nullable=False) 

    posts = relationship("Post", back_populates="user") 

class Post(Base):
    __tablename__ = 'posts' 

    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String(100), nullable=False) 
    content = Column(String(500), nullable=False) 
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) 
    
    user = relationship("User", back_populates="posts")  
