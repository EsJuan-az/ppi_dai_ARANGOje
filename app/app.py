from fastapi import FastAPI
from .routers.users import router as UserRouter 
from . import  models
from .database import engine
from .middlewares.exception import ExceptionHandlerMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
class App:
    def __init__(self):
        self._app = FastAPI()
        self.set_middlewares()
        self.set_exceptions()
        self.set_routes()
        self.set_db()
    
    def set_routes(self):
        self._app.include_router(UserRouter)
        
    def set_middlewares(self):
        self._app.add_middleware(ExceptionHandlerMiddleware)
        
    def set_exceptions(self):
        @self._app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, exc):
            err = exc.errors()
            return JSONResponse(
                content = {
                    "error": "Bad Request Error",
                    "message": err[0]['loc'][1] + " " + err[0]["type"]    
                },
                status_code = 400
                )
        @self._app.exception_handler(IntegrityError)
        async def integrity_error(request, exc):
            return JSONResponse(
                content = {
                    "error": "Bad Request Error",
                    "message": exc._message()
                },
                status_code = 400
                )
        
    def set_db(self):
        models.Base.metadata.create_all(bind=engine)
        
    def get_api(self):
        return self._app
    
    