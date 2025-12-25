from fastapi import APIRouter,Depends,File,UploadFile,Form
from app.utils.oauth2 import get_current_user
from app.core.responce import ApiResponse
from app.database.mongoDb import get_manual_collection
from cloudinary.uploader import upload
from app.core.responce import ApiError
from app.utils.cloudinary_config import cloudinary
from app.utils.qr import generate_qr_code,upload_qr_to_cloudinary
router = APIRouter(tags=["Upload manual"])

@router.post('/upload_file',response_model=dict)
async def uploadfile(company_name: str = Form(...),
    product_name: str = Form(...),
    file: UploadFile = File(...),
    curr_user:dict=Depends(get_current_user)):

    collection = get_manual_collection()

    if collection is None:
        raise ApiError(message="Manual Collection not found",status_code=500,errors="Internal servererror")
    
    print(file.file)
    result = upload(file.file , folder=f"manual/{company_name}",resource_type="auto")

    print(result)

    if result is None:
        raise ApiError(message="Unable to upload in claudinary",status_code=500,errors="Claudinary error")
    image_stream=generate_qr_code(company_name=company_name,product_name=product_name)
    qr=upload_qr_to_cloudinary(qr_buffer=image_stream,public_id=f"{company_name}_{product_name}")
    
    file_object = {
        "company_name":company_name,
        "product_name":product_name,
        "file_name":file.filename,
        "claudinary_file_url":result['url'],
        "cloudinary_file_public_id":result['public_id'],
        "claudinary_qr_url":qr['url'],
        "cloudinary_qr_public_id":qr['public_id'],
        "uploaded_by": curr_user
    }
    responce=collection.insert_one(file_object)

    if responce is None:
        raise ApiError(message="Unable to store in mongodb",status_code=500,errors="MongoDB error")

    return ApiResponse.success(data=str(file_object),status_code=200,message="Successfully stored and upload the file") 