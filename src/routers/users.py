from typing import List
from fastapi import  Depends, HTTPException, status, Path, APIRouter
# from requests import Session
from src.database.db import get_db
from src.database.models import User
from sqlalchemy.orm import Session, sessionmaker
from src.schemas import UserResponseModel, UserModel 


router = APIRouter(prefix='/users', tags=['users'])


@router.get("/", response_model=List[UserResponseModel]) #decorator route    return all owners from db
async def get_users(db: Session = Depends(get_db)):    #db: Session = Depends(get_db) - db is a variable, Session is a class
    owners = db.query(User).all()
    return owners



@router.get("/{user_id}", response_model=UserResponseModel) #decorator route    return all owners from db
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):    #db: Session = Depends(get_db) - db is a variable, Session is a class
    owner = db.query(User).filter_by(id=user_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return owner



@router.post("/", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED) #decorator route   return the created owner from
async def create_user(body: UserModel, db: Session = Depends(get_db)): #body: OwnerModel - body is a variable, OwnerModel is a class
    owner = db.query(User).filter_by(email=body.email).first()
    if owner:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    
    user = User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return owner


@router.put("/{user_id}", response_model=UserResponseModel) #decorator route, update   return the created owner from
async def update_user(body: UserModel,  owner_id: int = Path(ge=1), db: Session = Depends(get_db)): #body: OwnerModel - body is a variable, OwnerModel is a class
    owner = db.query(User).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    owner.email = body.email
    db.commit()
    db.refresh(owner)
    return owner


@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT) #decorator route, delete,   return the created owner from
async def delete_user(owner_id: int = Path(ge=1), db: Session = Depends(get_db)): #body: OwnerModel - body is a variable, OwnerModel is a class
    owner = db.query(User).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(owner)
    db.commit(owner)
    return owner