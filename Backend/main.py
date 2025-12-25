from fastapi import FastAPI,Request
from app.database.mongoDb import connect_to_mongo, close_mongo_connection
from fastapi.responses import JSONResponse
from app.api.routes.user import router as user_router
from app.api.routes.upload import router as menual_router
from app.core.responce import ApiError
app = FastAPI(title="Companion AI Backend")

@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "errors": exc.errors
        }
    )
@app.on_event("startup")
def startup():
    connect_to_mongo()

@app.on_event("shutdown")
def shutdown():
    close_mongo_connection()

# routers
app.include_router(user_router)
app.include_router(menual_router)


@app.get("/")
def root():
    return {"message": "Companion AI API is running"}



