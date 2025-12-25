import qrcode
import json
import io
from fastapi import HTTPException
from cloudinary.uploader import upload
from app.utils.cloudinary_config import cloudinary
def generate_qr_code(company_name:str,product_name:str)-> io.BytesIO:
    try:
        data={
            "company_name":company_name,
            "product_name":product_name,
        }
        qr=qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(json.dumps(data))
        qr.make(fit=True)

        img=qr.make_image(fill_color="black",back_color="white")

        qr_buffer=io.BytesIO()
        img.save(qr_buffer,format='PNG')
        qr_buffer.seek(0)  
        return qr_buffer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QR code generation failed: {str(e)}")

def upload_qr_to_cloudinary(qr_buffer: io.BytesIO, public_id: str) -> dict:
    """
    Upload QR code to Cloudinary and return the upload result
    """
    try:
        result = upload(
            qr_buffer,
            resource_type="image",  # For QR code images
            public_id=public_id,
            folder="qr_codes"  # Organize QR codes in a folder
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QR code Cloudinary upload failed: {str(e)}")