from fastapi import APIRouter
from bson import ObjectId
from typing import List
from app.core.responce import ApiResponse
from app.schema import userSchema
from app.database import mongoDb
from app.utils.hashing import Hash
from app.utils.JWTtoken import create_access_token
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()



router = APIRouter(tags=["User"])

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.post('/create_user',response_model=dict)
async def create_user(request : userSchema.CreateUser):
    collection = mongoDb.get_user_collection()

    if not collection:
        return ApiResponse.error(message="User collection not found",status_code=500,errors="Internal server error")

    hashed_pass = Hash.bcrypt(request.password)
    email = request.email.strip().lower()
    user_data = {
        "username" : request.username,
        "email" : email,
        "password" : hashed_pass,
        "role" : "user"
    }

    user = collection.insert_one(user_data)

    if not user:
        return ApiResponse.error(message="User not created!",status_code=500,errors="Internal server error")
    
    return ApiResponse.success(message="User created successfully",data=str(user.inserted_id),status_code=201)




@router.post('/login',response_model=dict)
async def login(request : userSchema.login):
    collection = mongoDb.get_user_collection()

    if not collection:
        return ApiResponse.error(message="User collection not found",status_code=500,errors="Internal server error")
    
    email = request.email.strip().lower()
    user = collection.find_one({"email" : email})
    print("user :" ,user)

    if not user:
        return ApiResponse.error(message="Email has been not registed",status_code=401,errors="Unvalide creadential")

    check_psw = Hash.verify(plain_password=request.password,hashed_password= user["password"])

    if not check_psw:
        return ApiResponse.error(message="Please enter valid password",status_code=401,errors="Not valid password")
    

    user["_id"] = str(user["_id"])
    user.pop("password", None)

    access_token = create_access_token(
    data={"sub": user["email"]},
    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return ApiResponse.success(data=access_token,message="Login successfully",status_code=200)

@router.get("/user_data",response_model=dict)
async def user():
    collection = mongoDb.get_user_collection()
    users=collection.find({})
    users_list=[]
    for user in users:
        temp={
            "_id":str(user["_id"]),
            "email":user["email"]
        }
        users_list.append(temp)
    return ApiResponse.success(data=users_list,status_code=200,message="user details are fetched")
    
