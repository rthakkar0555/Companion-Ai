from typing import Any, Optional
from fastapi.responses import JSONResponse

@staticmethod
def error(
    message: str = "Something went wrong",
    status_code: int = 400,
    errors: Optional[Any] = None
):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "errors": errors
        }
    )