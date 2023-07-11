import os
import pickle

from datetime import datetime, timedelta
from typing import Optional


import redis
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer #Bearer token
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette import status

from src.database import get_db, User

from src.conf.config import settings


class Hash:
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and the hashed version of that password,
            and returns True if they match, False otherwise.
        
        
        :param self: Make the method a bound method, which means that it can be called on instances of the class
        :param plain_password: Pass in the password that is entered by the user
        :param hashed_password: Compare the plain_password to the hashed password
        :return: True if the password matches the hash, otherwise it returns false
        :doc-author: Trelent
        """
        
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password as an argument and returns the hash of that password.
            The function uses the pwd_context object to generate a hash from the given password.
        
        :param self: Represent the instance of the class
        :param password: str: Get the password from the user
        :return: The hashed password
        :doc-author: Trelent
        """
        
        return self.pwd_context.hash(password)

class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    
    
    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and the hashed version of that password,
            and returns True if they match, False otherwise.
        
        
        :param self: Make the function a method of the user class
        :param plain_password: Check the password that is entered by the user
        :param hashed_password: Compare the hashed password in the database with a plain text password
        :return: True if the password is correct and false otherwise
        :doc-author: Trelent
        """
        
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)
    
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None): #
        """
        The create_access_token function creates a new access token for the user.
            
        
        :param self: Represent the instance of the class
        :param data: dict: Pass the data that will be encoded into the token
        :param expires_delta: Optional[float]: Set the time for which the token is valid
        :return: A token that is encoded with the user's information
        :doc-author: Trelent
        """
        
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token
    
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None): #
        """
        The create_refresh_token function creates a refresh token for the user.
            Args:
                data (dict): A dictionary containing the user's id and username.
                expires_delta (Optional[float]): The number of seconds until the refresh token expires. Defaults to None, which sets it to 7 days from now.
        
        :param self: Represent the instance of the class
        :param data: dict: Pass the user's information to be encoded in the token
        :param expires_delta: Optional[float]: Set the expiration time of the refresh token
        :return: A jwt encoded with the user's id and a refresh token scope
        :doc-author: Trelent
        """
        
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be used in the UserRouter class.
        It takes an access token as input and returns the user object associated with it.
        
        
        :param self: Represent the instance of a class
        :param token: str: Get the token from the header of the request
        :param db: Session: Get the database session
        :return: An object of the user class, which contains an email and a password
        :doc-author: Trelent
        """
        
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == "access_token":
                email = payload.get("sub")
                if email is None:
                    raise credentials_exception
                else:
                    raise credentials_exception
        except JWTError as e:
            raise credentials_exception
        
        # user = await repository.get_user_by_email(db, email=email)
        
        user = self.r.get(f"user:{email}")
        if user is None:
            user = await repository.get_user_by_email(db, email=email)
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{email}", pickle.dumps(user))
            self.r.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
            
        if user is None:
            raise credentials_exception
        return user
    
    async def decode_refresh_token(self, refresh_token: str ):
        """
        The decode_refresh_token function takes a refresh token as an argument and returns the email of the user who owns that refresh token.
            If the decode_refresh_token function is unable to decode a valid JWT, it will raise an HTTPException with status code 401 (Unauthorized).
        
        
        :param self: Represent the instance of the class
        :param refresh_token: str: Pass the refresh token to the function
        :return: The email of the user who is trying to refresh his token
        :doc-author: Trelent
        """
        
        try:   
            # Decode JWT
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == "refresh_token":
                email = payload.get("sub")
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
                
            
    def create_email_token(self, data: dict):
        """
        The create_email_token function creates a JWT token that is used to verify the user's email address.
            The token contains the following data:
                - iat (issued at): The time when the token was created.
                - exp (expiration): When this token expires and becomes invalid.  This is set to 1 minute from creation time, so it should be used immediately after being generated.
                - scope: A string indicating what this JWT can be used for; in this case, &quot;email_token&quot;.  This will help us determine how we want to handle each type of JWT later on in our codebase
        
        :param self: Make the function a method of the class
        :param data: dict: Pass in the data that will be encoded
        :return: A token
        :doc-author: Trelent
        """
        
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=1)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token      
    
    def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email associated with that token.
            If the token is invalid, it raises an HTTPException.
        
        :param self: Represent the instance of the class
        :param token: str: Pass the token that is sent from the frontend to be decoded
        :return: The email address associated with the token
        :doc-author: Trelent
        """
        
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == "email_token":
                email = payload.get("sub")
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid token")
    

# SECRET_KEY = "secret_key"
# ALGORITHM = "HS256"

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# # token_scheme = HTTPBearer() #Bearer token


# # define a function to generate a new access token
# async def create_access_token(data: dict, expires_delta: Optional[float] = None): #
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + timedelta(seconds=expires_delta)
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         # Decode JWT
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get(["sub"])
#         if email is None:
#             raise credentials_exception
#     except JWTError as e:
#         raise credentials_exception

#     # user: User = db.query(User).filter(User.email == email).first()
#     user: User| None = db.query(User).filter.by(email = email).first()
#     if user is None:
#         raise credentials_exception
#     return user

auth_service = Auth()