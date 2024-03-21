from fastapi import FastAPI
from .routers.users import router as UserRouter 
from .routers.business import router as BusinessRouter 
from .routers.product import router as ProductRouter 

from . import  models
from .database import engine
from .middlewares.exception import ExceptionHandlerMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
class App:
    def __init__(self):
        self._app = FastAPI()
        self.set_middlewares()
        self.set_exceptions()
        self.set_routes()
        self.set_db()
    
    def set_routes(self):
        self._app.include_router(UserRouter)
        self._app.include_router(BusinessRouter)
        self._app.include_router(ProductRouter)
        
        
    def set_middlewares(self):
        self._app.add_middleware(ExceptionHandlerMiddleware)
        
    def set_exceptions(self):
        @self._app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, exc):
            return JSONResponse(
                content = {
                    "detail": "Invalid Credentials",
                    "message": exc.errors()
                },
                status_code = 400
                )
        @self._app.exception_handler(IntegrityError)
        async def integrity_error(request, exc):
            return JSONResponse(
                content = {
                    "detail": "Invalid Credentials",
                    "message": exc._message()
                },
                status_code = 400
                )
        @self._app.exception_handler(NoResultFound)
        async def not_result_found(request, exc):

            return JSONResponse(
                content = {
                    "detail": "Not Found",
                    "message": exc._message()
                },
                status_code = 404
                )
            
        
    def set_db(self):
        models.Base.metadata.create_all(bind=engine)
        
    def get_api(self):
        return self._app
    
    