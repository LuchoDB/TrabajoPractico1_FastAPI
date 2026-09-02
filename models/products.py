from pydantic import BaseModel, Field
from typing import List, Optional

class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float = Field(..., gt=0, description="Precio del producto, debe ser mayor a cero")
    stock: int = Field(..., ge=0, description="Cantidad en stock, no puede ser negativa")
    is_active: bool = True

class GetProductsResponse(BaseModel):
    products: List[Product]

class CreateProductResponse(Product):
    message: str

class DeleteProductResponse(BaseModel):
    message: str

class UpdateProductRequest(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class UpdateProductResponse(Product):
    message: str
