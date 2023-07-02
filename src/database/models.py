from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), unique=True, index=True)
    full_name = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    phone_number = Column(String(50), unique=True, index=True)
    bith_date = Column(String(50), unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
   
    