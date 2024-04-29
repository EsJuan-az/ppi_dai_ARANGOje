# Librerías para manejar las peticiones y los errores.
import logging
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
# Excepciones que voy a manejar en el middleware.
from fastapi.exceptions import FastAPIError
from sqlalchemy.exc import SQLAlchemyError
# Funciones de procesamiento de texto para el mensaje.
from ..helpers.error_helper import extract_field_from_integrity
logger = logging.getLogger(__name__)

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware para manejar excepciones: Desde aquí diseño una respuesta adecuada para
    cada tipo distinto de error.
    Extends:
        BaseHTTPMiddleware: clase Middleware para fastAPI
    """
    async def dispatch(self, request: Request, call_next):
        """Maneja los errores HTTP recibidos desde los controladores
        Args:
            request (Request): Petición que despertó el error.
            call_next (func): Callback para continuar la ejecución.
        """
        try:
            return await call_next(request)
        except SQLAlchemyError as exc:
            sql_message = exc._sql_message()
            field = extract_field_from_integrity( sql_message )
            msg = 'Base de datos sin conexión'
            if field:
                msg = f'{field} ya está en uso'
            elif 'No row was found when one was required' in sql_message:
                msg = 'Credenciales inválidos'
            return JSONResponse(
                status_code = 408,
                content = {
                    "error": "Database Client Error",
                    "message": msg,
                },
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
                content={"error": "Internal Server Error", "message": "Ha ocurrido un error inesperado."},
            )