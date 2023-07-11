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
    """
    The get_users function returns a list of all users in the database.
        :return: A list of dictionaries containing user information.
    
    :param db: Session: Get the database session
    :return: A list of users
    :doc-author: Trelent
    """
    
    owners = db.query(User).all()
    return owners



@router.get("/{user_id}", response_model=UserResponseModel) #decorator route    return all owners from db
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):    #db: Session = Depends(get_db) - db is a variable, Session is a class
    """
    The get_user function returns a user object based on the id passed in.
        If no user is found, it will return an HTTP 404 error.
    
    :param user_id: int: Get the user id from the path, and db: session = depends(get_db) is used to connect to the database
    :param db: Session: Pass the database session to the function
    :return: The owner of the item, so it returns a user object
    :doc-author: Trelent
    """
    
    owner = db.query(User).filter_by(id=user_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return owner



@router.post("/", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED) #decorator route   return the created owner from
async def create_user(body: UserModel, db: Session = Depends(get_db)): #body: OwnerModel - body is a variable, OwnerModel is a class
    """
    The create_user function creates a new user in the database.
        It takes an email and password as input, hashes the password, and stores it in the database.
        The function returns a UserModel object with all of its fields filled out.
    
    :param body: UserModel: Get the data from the request body
    :param db: Session: Get the database session
    :return: The owner object
    :doc-author: Trelent
    """
    
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
    """
    The update_user function updates a user in the database.
        The function takes an owner_id and a body as input, where the body is of type OwnerModel.
        If no owner with that id exists, it raises an HTTPException with status code 404 (Not Found). 
        Otherwise, it updates the email field of that user to be equal to what was passed in through the request body. 
    
    
    :param body: UserModel: Get the data from the request body
    :param owner_id: int: Get the id of the owner from the url
    :param db: Session: Get the database session
    :return: The updated user object
    :doc-author: Trelent
    """
    
    owner = db.query(User).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    owner.email = body.email
    db.commit()
    db.refresh(owner)
    return owner


@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT) #decorator route, delete,   return the created owner from
async def delete_user(owner_id: int = Path(ge=1), db: Session = Depends(get_db)): #body: OwnerModel - body is a variable, OwnerModel is a class
    """
    The delete_user function deletes a user from the database.
        The function takes in an owner_id as a path parameter and uses it to find the user in the database.
        If no such user is found, then an HTTPException is raised with status code 404 (Not Found). 
        Otherwise, if such a user exists, then that particular row of data is deleted from the table.
    
    :param owner_id: int: Specify the id of the owner that will be deleted
    :param db: Session: Access the database
    :return: The deleted owner
    :doc-author: Trelent
    """
    
    owner = db.query(User).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(owner)
    db.commit(owner)
    return owner