from fastapi import FastAPI
from routers.users import router as users_router
from routers.products import router as products_router

app = FastAPI(
    title="API ABM - Programacion 4 (FastAPI)",
    description=(
        "API REST para la gestión y ABM completo de Usuarios y Productos (Entidad propia) "
        "con almacenamiento en memoria y modelos de validación Pydantic."
    ),
    version="1.0.0",
    redoc_url=None,
)

# Inclusión de routers
# Prefijo estándar /users y alias /user para compatibilidad con la clase
app.include_router(users_router, prefix="/users")
app.include_router(users_router, prefix="/user", include_in_schema=False)

# Prefijo estándar /products y alias /producto para la entidad propia
app.include_router(products_router, prefix="/products")
app.include_router(products_router, prefix="/producto", include_in_schema=False)


@app.get("/", summary="Endpoint raíz de bienvenida")
def read_root():
    return {
        "message": "Bienvenido a la API del Trabajo Practico 1 - Programacion 4",
        "docs": "/docs",
        "endpoints": {
            "usuarios": "/users",
            "productos": "/products",
        },
    }