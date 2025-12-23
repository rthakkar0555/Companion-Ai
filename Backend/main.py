from fastapi import FastAPI
from app.database.mongoConnection import connect_to_mongo, close_mongo_connection

app = FastAPI(title="Companion AI Backend")

@app.on_event("startup")
def startup():
    connect_to_mongo()

@app.on_event("shutdown")
def shutdown():
    close_mongo_connection()

@app.get("/")
def root():
    return {"message": "Companion AI API is running"}
