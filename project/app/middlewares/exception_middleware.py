import logging
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
# EXCEPTIONS
from fastapi import Request, HTTPException
from fastapi.exceptions import FastAPIError
from sqlalchemy.exc import SQLAlchemyError
logger = logging.getLogger(__name__)

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as http_exception:
            return JSONResponse(
                status_code=http_exception.status_code,
                content={"error": "Client Error", "message": str(http_exception.detail)},
            )
        except SQLAlchemyError as exc:
            return JSONResponse(
                status_code = 408,
                content={"error": "Database Client Error", "message": str(exc._message())},
            )
        except FastAPIError as exc:
            return JSONResponse(
                status_code = 500,
                content={"error": "Internal Server Error", "message": str(exc.errors())},
            )
        except Exception as e:
            logger.exception(msg=e.__class__.__name__)
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error", "message": "An unexpected error occurred."},
            )