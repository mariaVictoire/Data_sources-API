from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api.router import router 
from src.api.routes.data import router as data_router
from src.api.routes.parameters import router as parameters_router
from src.api.routes.authentication import router as authentification_router
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
swagger_token = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentification/login")

def custom_openapi():
    """Personnalisation du schéma OpenAPI."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="epf-flower-data-science",
        version="1.0.0", 
        description="Fast API avec JWT Bearer Token",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",  
        }
    }
    # Appliquer BearerAuth sur toutes les routes
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema
 


def get_application() -> FastAPI:
    application = FastAPI(
        title="epf-flower-data-science",
        description="""Fast API""",
        version="1.0.0",
        redoc_url=None,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router)
    application.include_router(data_router, prefix="/data", tags=["data"])
    application.include_router(parameters_router, prefix="/parameters", tags=["parameters"])
    application.include_router(authentification_router, prefix="/authentification", tags=["authentification"])
    application.openapi = custom_openapi

    return application

app = get_application()