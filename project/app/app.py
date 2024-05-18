# THIRD PARTY LIBS:
from fastapi import FastAPI, HTTPException, Request
from .middlewares.exception_middleware import ExceptionHandlerMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware



# HELPERS

# ROUTERS
from .routers.user_router import router as UserRouter 
from .routers.business_router import router as BusinessRouter 
from .routers.product_router import router as ProductRouter 
from .routers.shopkeeper_router import router as ShopkeeperRouter 
from .routers.order_router import router as OrderRouter 
from .routers.record_router import router as RecordRouter 


    
class App:
    def __init__(self):
        """Setting inicial: Añade middlewares, rutas y evento de creación.
        Args:
        Return:
        """
        self._app = FastAPI()
        self.set_errors()
        self.set_middlewares()
        self.set_routes()
    
    
    def set_errors(self):
        """Maneja algunos errores que no alcanzan los middlewares.
        Args:
        Return:
        """
        @self._app.exception_handler(HTTPException)
        async def http_exc_handler(request: Request, http_exception: HTTPException):
            return JSONResponse(
                status_code=http_exception.status_code,
                content={
                    "error": "Client Error",
                    "message": str(http_exception.detail),
                }, 
            )
            
    
    def set_routes(self):
        """Rutas: Añade las rutas por defecto y añade un método de ping.
        Args:
        Return:
        """
        @self._app.get('/')
        def ping():
            """Esta función maneja la petición básica para
            un healthchek.

            Returns:
                dict: Dummy data para obtener.
            """
            return {
                'ping': 'pong',
            }
        self._app.include_router(UserRouter)
        self._app.include_router(BusinessRouter)
        self._app.include_router(ProductRouter)
        self._app.include_router(ShopkeeperRouter)
        self._app.include_router(OrderRouter)
        self._app.include_router(RecordRouter)
        
        
        
    def set_middlewares(self):
        """Middlewares: Añade gestión de errores y manejo de peticiones externas.
        Args:
        Returns:
        """
        self._app.add_middleware(ExceptionHandlerMiddleware)
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def get_api(self):
        return self._app
    
    