from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from models.products import (
    Product,
    GetProductsResponse,
    CreateProductResponse,
    DeleteProductResponse,
    UpdateProductRequest,
    UpdateProductResponse,
)

router = APIRouter(tags=["Productos"])

# Almacenamiento en memoria para la entidad propia (Producto)
productos: List[Product] = [
    Product(
        id=1,
        name="Notebook Lenovo ThinkPad",
        category="Computación",
        price=1250.0,
        stock=15,
        is_active=True,
    ),
    Product(
        id=2,
        name="Mouse Inalámbrico Logitech",
        category="Periféricos",
        price=45.5,
        stock=50,
        is_active=True,
    ),
    Product(
        id=3,
        name="Teclado Mecánico RGB",
        category="Periféricos",
        price=95.0,
        stock=0,
        is_active=False,
    ),
    Product(
        id=4,
        name="Monitor 27 Pulgadas IPS 144Hz",
        category="Monitores",
        price=320.0,
        stock=8,
        is_active=True,
    ),
]


@router.get("", response_model=GetProductsResponse, summary="Listar y filtrar productos")
@router.get("/", response_model=GetProductsResponse, include_in_schema=False)
def get_products(
    category: Optional[str] = Query(
        None,
        description="Filtrar por categoría exacta (ej: 'Computación', 'Periféricos')",
    ),
    name: Optional[str] = Query(
        None,
        description="Buscar productos por texto contenido en el nombre",
    ),
    is_active: Optional[bool] = Query(
        None,
        description="Filtrar por disponibilidad: true (activos), false (inactivos)",
    ),
    min_price: Optional[float] = Query(
        None,
        ge=0,
        description="Filtrar productos con precio mayor o igual a este valor",
    ),
    max_price: Optional[float] = Query(
        None,
        ge=0,
        description="Filtrar productos con precio menor o igual a este valor",
    ),
) -> GetProductsResponse:
    resultado = productos

    if category is not None:
        resultado = [p for p in resultado if p.category.lower() == category.lower()]

    if name is not None:
        resultado = [p for p in resultado if name.lower() in p.name.lower()]

    if is_active is not None:
        resultado = [p for p in resultado if p.is_active == is_active]

    if min_price is not None:
        resultado = [p for p in resultado if p.price >= min_price]

    if max_price is not None:
        resultado = [p for p in resultado if p.price <= max_price]

    return GetProductsResponse(products=resultado)


@router.get("/{id}", response_model=Product, summary="Obtener producto por ID")
def get_product_by_id(id: int) -> Product:
    for prod in productos:
        if prod.id == id:
            return prod
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El producto {id} no existe",
    )


@router.post(
    "",
    response_model=CreateProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo producto",
)
@router.post(
    "/",
    response_model=CreateProductResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_product(product: Product) -> CreateProductResponse:
    for existing in productos:
        if existing.id == product.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El producto con id {product.id} ya existe",
            )
    productos.append(product)
    return CreateProductResponse(
        id=product.id,
        name=product.name,
        category=product.category,
        price=product.price,
        stock=product.stock,
        is_active=product.is_active,
        message="Producto creado exitosamente",
    )


@router.put(
    "/{id}",
    response_model=UpdateProductResponse,
    summary="Modificar producto (PUT)",
)
def update_product_put(id: int, product_data: UpdateProductRequest) -> UpdateProductResponse:
    for prod in productos:
        if prod.id == id:
            if product_data.name is not None:
                prod.name = product_data.name
            if product_data.category is not None:
                prod.category = product_data.category
            if product_data.price is not None:
                prod.price = product_data.price
            if product_data.stock is not None:
                prod.stock = product_data.stock
            if product_data.is_active is not None:
                prod.is_active = product_data.is_active
            return UpdateProductResponse(
                id=prod.id,
                name=prod.name,
                category=prod.category,
                price=prod.price,
                stock=prod.stock,
                is_active=prod.is_active,
                message=f"El producto {id} ha sido modificado correctamente",
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El producto {id} no existe",
    )


@router.patch(
    "/{id}",
    response_model=UpdateProductResponse,
    summary="Modificar producto parcialmente (PATCH)",
)
def update_product_patch(id: int, product_data: UpdateProductRequest) -> UpdateProductResponse:
    return update_product_put(id=id, product_data=product_data)


@router.delete(
    "/{id}",
    response_model=DeleteProductResponse,
    summary="Eliminar producto por ID",
)
def delete_product(id: int) -> DeleteProductResponse:
    for prod in productos:
        if prod.id == id:
            productos.remove(prod)
            return DeleteProductResponse(
                message=f"El producto {id} ha sido eliminado correctamente"
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El producto {id} no existe",
    )
