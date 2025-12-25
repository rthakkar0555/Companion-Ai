from fastapi import APIRouter,Depends
from bson import ObjectId
from typing import List
from app.core.responce import ApiResponse,ApiError
from app.schema import userSchema
from app.database import mongoDb
from app.utils.hashing import Hash
from app.utils.JWTtoken import create_access_token
from dotenv import load_dotenv
from app.utils.oauth2 import get_current_user
import os
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

load_dotenv()

router = APIRouter(tags=["User"])

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.post('/create_user',response_model=dict)
async def create_user(request : userSchema.CreateUser):
    collection = mongoDb.get_user_collection()

    if collection is None:
        return ApiError(message="User collection not found",status_code=500,errors="Internal server error")

    hashed_pass = Hash.bcrypt(request.password)
    email = request.email.strip().lower()
    user_data = {
        "username" : request.username,
        "email" : email,
        "password" : hashed_pass,
        "role" : "user"
    }

    user = collection.insert_one(user_data)

    if user is None:
        return ApiError(message="User not created!",status_code=500,errors="Internal server error")
    
    return ApiResponse.success(message="User created successfully",data=str(user.inserted_id),status_code=201)




@router.post('/login',response_model=dict)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    collection = mongoDb.get_user_collection()

    if collection is None:
        return ApiError(message="User collection not found",status_code=500,errors="Internal server error")
    
    email = request.username.strip().lower()
    user = collection.find_one({"email" : email})
    print("user :" ,user)

    if not user:
        return ApiError(message="Email has been not registed",status_code=401,errors="Unvalide creadential")

    check_psw = Hash.verify(plain_password=request.password,hashed_password= user["password"])

    if not check_psw:
        return ApiError(message="Please enter valid password",status_code=401,errors="Not valid password")
    

    user["_id"] = str(user["_id"])
    user.pop("password", None)

    access_token = create_access_token(
    data={"sub": user["email"]},
    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    data={
        "access_token":access_token,
        "token_type":"bearer"
    }

    return data

@router.get("/user_data",response_model=dict)
async def user(x:dict=Depends(get_current_user)):
    collection = mongoDb.get_user_collection()
    users=collection.find({})
    users_list=[]
    for user in users:
        temp={
            "_id":str(user["_id"]),
            "email":user["email"]
        }
        users_list.append(temp)
    return ApiResponse.success(data=str(users_list),status_code=200,message="user details are fetched")
    
