from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List, Optional
from models.users import (
    User,
    GetUsersResponse,
    CreateUserResponse,
    DeleteUserResponse,
)

router = APIRouter(tags=["Usuarios"])


# Esquema para actualización parcial o total sin alterar models/users.py
class UpdateUserRequest(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None


# Almacenamiento en memoria
usuarios: List[User] = [
    User(id=1, name="Luciano Diaz", is_active=True),
    User(id=2, name="Ana Lopez", is_active=True),
    User(id=3, name="Carlos Gomez", is_active=False),
]


@router.get("", response_model=GetUsersResponse, summary="Listar usuarios")
@router.get("/", response_model=GetUsersResponse, include_in_schema=False)
def get_users(
    is_active: Optional[bool] = Query(
        None,
        description="Filtrar por estado: true (activos), false (inactivos) o omitir para listar todos",
    ),
    is_activ: Optional[bool] = Query(
        None,
        include_in_schema=False,
        description="Alias de compatibilidad para is_active",
    ),
) -> GetUsersResponse:
    filtro_estado = is_active if is_active is not None else is_activ

    if filtro_estado is None:
        return GetUsersResponse(users=usuarios)

    filtrados = [user for user in usuarios if user.is_active == filtro_estado]
    return GetUsersResponse(users=filtrados)


@router.get("/{id}", response_model=User, summary="Obtener usuario por ID")
def get_user_by_id(id: int) -> User:
    for user in usuarios:
        if user.id == id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El usuario {id} no existe",
    )


@router.post(
    "",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
)
@router.post(
    "/",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_user(user: User) -> CreateUserResponse:
    for existing_user in usuarios:
        if existing_user.id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El usuario con id {user.id} ya existe",
            )
    usuarios.append(user)
    return CreateUserResponse(
        id=user.id,
        name=user.name,
        is_active=user.is_active,
        message="Usuario creado exitosamente",
    )


@router.put(
    "/{id}",
    response_model=CreateUserResponse,
    summary="Modificar usuario (PUT)",
)
def update_user_put(id: int, user_data: UpdateUserRequest) -> CreateUserResponse:
    for user in usuarios:
        if user.id == id:
            if user_data.name is not None:
                user.name = user_data.name
            if user_data.is_active is not None:
                user.is_active = user_data.is_active
            return CreateUserResponse(
                id=user.id,
                name=user.name,
                is_active=user.is_active,
                message=f"El usuario {id} ha sido modificado correctamente",
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El usuario {id} no existe",
    )


@router.patch(
    "/{id}",
    response_model=CreateUserResponse,
    summary="Modificar usuario parcialmente (PATCH)",
)
def update_user_patch(id: int, user_data: UpdateUserRequest) -> CreateUserResponse:
    return update_user_put(id=id, user_data=user_data)


@router.delete(
    "/{id}",
    response_model=DeleteUserResponse,
    summary="Eliminar usuario por ID",
)
def delete_user(id: int) -> DeleteUserResponse:
    for user in usuarios:
        if user.id == id:
            usuarios.remove(user)
            return DeleteUserResponse(
                message=f"El usuario {id} ha sido eliminado correctamente"
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El usuario {id} no existe",
    )