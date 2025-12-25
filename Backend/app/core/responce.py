from typing import Any, Optional
from fastapi.responses import JSONResponse
from typing import Any, Optional
class ApiResponse:

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = 200
    ):
        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": data
            }
        )

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


class ApiError(Exception):
    def __init__(
        self,
        message: str = "Something went wrong",
        status_code: int = 400,
        errors: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.errors = errors
        super().__init__(message)