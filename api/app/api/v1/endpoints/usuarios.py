"""Endpoints de gestión de usuarios."""

from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import Optional
from app.schemas.usuarios import UsuarioResponse, UsuarioCreate, UsuarioUpdate, UsuarioPaginated
from app.services import usuarios as user_service
from app.core.dependencies import get_current_user_id

router = APIRouter()

@router.get("/me", response_model=UsuarioResponse)
def get_current_user_profile(user_id: int = Depends(get_current_user_id)):
    """Obtiene el perfil del usuario autenticado desde el token JWT."""
    user = user_service.obtener_usuario_por_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.get("/stats")
def get_user_stats():
    """Estadísticas de usuarios: total, roles y estados."""
    return user_service.obtener_stats_usuarios()

@router.get("/", response_model=UsuarioPaginated)
def get_users(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    rol: Optional[int] = None, 
    estado: Optional[str] = None, 
    query: Optional[str] = None
):
    """Lista paginada de usuarios con filtros."""
    result = user_service.obtener_usuarios(skip=skip, limit=limit, rol=rol, estado=estado, query=query)
    return {
        "total": result["total"],
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "limit": limit,
        "data": result["data"]
    }

@router.post("/", response_model=dict)
def create_user(usuario: UsuarioCreate):
    """Registra un nuevo usuario."""
    user_id = user_service.crear_usuario(usuario)
    if not user_id:
        raise HTTPException(status_code=400, detail="Error creando usuario")
    return {"message": "Usuario creado exitosamente", "id_usuario": user_id}

@router.get("/{id_usuario}", response_model=UsuarioResponse)
def get_user(id_usuario: int):
    """Obtiene un usuario por ID."""
    user = user_service.obtener_usuario_por_id(id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{id_usuario}", response_model=UsuarioResponse)
def update_user(id_usuario: int, usuario: UsuarioUpdate):
    """Actualiza un usuario existente."""
    exito = user_service.actualizar_usuario(id_usuario, usuario)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no modificado")
    return user_service.obtener_usuario_por_id(id_usuario)

@router.delete("/{id_usuario}", response_model=dict)
def delete_user(id_usuario: int):
    """Elimina un usuario."""
    exito = user_service.eliminar_usuario(id_usuario)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}

