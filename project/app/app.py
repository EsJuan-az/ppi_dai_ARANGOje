# THIRD PARTY LIBS:
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .middlewares.exception_middleware import ExceptionHandlerMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


# HELPERS
from .database import db_startup

# ROUTERS
from .routers.user_router import router as UserRouter 
from .routers.business_router import router as BusinessRouter 
from .routers.product_router import router as ProductRouter 
from .routers.shopkeeper_router import router as ShopkeeperRouter 


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_startup()
    yield
    
    
class App:
    def __init__(self):
        """Setting inicial: Añade middlewares, rutas y evento de creación.
        """
        self._app = FastAPI(
            lifespan = lifespan,
        )
        self.set_middlewares()
        self.set_routes()
    
    def set_routes(self):
        """Rutas: Añade las rutas por defecto y añade un método de ping.
        """
        @self._app.get('/')
        def ping():
            return {
                'ping': 'pong',
            }
        self._app.include_router(UserRouter)
        self._app.include_router(BusinessRouter)
        self._app.include_router(ProductRouter)
        self._app.include_router(ShopkeeperRouter)
        
        
    def set_middlewares(self):
        """Middlewares: Añade gestión de errores y manejo de peticiones externas.
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
    
    