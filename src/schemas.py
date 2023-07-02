# Validation schemas for the API    
from pydantic import BaseModel, Field, validator, EmailStr

class UserModel(BaseModel):
    
    first_name: str = Field("John", title="First Name", max_length=50)
    full_name: str = Field("John Doe", title="Full Name", max_length=50)
    email: EmailStr
    phone_number: str = Field("1234567890", title="Phone Number", max_length=50)
    bith_date:str = Field("01/01/2000", title="Birth Date", max_length=50)
    created_at = Field("01/01/2000", title="Created At")
    updated_at = Field("01/01/2000", title="Updated At")
    
    
class UserResponseModel(BaseModel): 
    
    id: int = 1 #Field(..., title="User ID")
    first_name: str = Field("John", title="First Name", max_length=50)
    full_name: str = Field("John Doe", title="Full Name", max_length=50)
    phone_number: str = Field("1234567890", title="Phone Number", max_length=50)
    bith_date:str = Field("01/01/2000", title="Birth Date", max_length=50)
    created_at = Field("01/01/2000", title="Created At")
    updated_at = Field("01/01/2000", title="Updated At")
    
    class Config:
        orm_mode = True
       
    
 