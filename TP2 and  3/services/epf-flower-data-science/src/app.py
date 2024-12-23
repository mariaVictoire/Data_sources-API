from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from src.api.router import router 
from src.api.routes.data import router as data_router
from src.api.routes.parameters import router as parameters_router
from src.api.routes.authentication import router as authentification_router
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
swagger_token = None

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentification/login")

limiter = Limiter(key_func=get_remote_address)

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
 

#  Configurer le Middleware Rate Limiting 
async def rate_limit_middleware(request: Request, call_next):
    """Middleware pour gérer les limites de requêtes globales."""
    try:
        response = await call_next(request)
        return response
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Trop de requêtes. Réessayez plus tard.")


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

    # Ajouter le middleware SlowAPI pour le rate limiting
    application.state.limiter = limiter
    application.add_middleware(SlowAPIMiddleware)
 
    # Ajouter le middleware personnalisé pour les requêtes
    application.middleware("http")(rate_limit_middleware)


    application.include_router(router)
    application.include_router(data_router, prefix="/v0/data", tags=["data"])
    application.include_router(parameters_router, prefix="/v0/parameters", tags=["parameters"])
    application.include_router(authentification_router, prefix="/v0/authentification", tags=["authentification"])
    application.openapi = custom_openapi

    # Ajout de la configuration personnalisée pour Swagger
    application.openapi = custom_openapi

    # --- Gestion des erreurs personnalisées ---
    @application.exception_handler(404)
    async def custom_404_handler(request: Request, exc: HTTPException):
        """Gestionnaire d'erreur personnalisé pour 404."""
        return HTTPException(
            status_code=404,
            detail=f"Route '{request.url.path}' introuvable. Vérifiez l'URL et réessayez."
        )
 

    return application

app = get_application()
 

 
 

 

 
