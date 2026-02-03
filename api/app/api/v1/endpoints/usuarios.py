# Endpoints para la Gestión de Usuarios
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from app.schemas.usuarios import UsuarioResponse, UsuarioCreate, UsuarioUpdate, UsuarioPaginated
from app.services import usuarios as user_service
from app.core.dependencies import get_current_user_id

router = APIRouter()

@router.get("/me", response_model=UsuarioResponse)
def get_my_profile(user_id: int = Depends(get_current_user_id)):
    """Obtiene el perfil del usuario autenticado."""
    user = user_service.obtener_usuario_por_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.get("/stats")
def get_user_stats(current_user_id: int = Depends(get_current_user_id)):
    """Obtiene estadísticas generales de los usuarios (requiere autenticación)."""
    return user_service.obtener_stats_usuarios()

@router.get("/", response_model=UsuarioPaginated)
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    rol: Optional[int] = None, 
    estado: Optional[str] = None, 
    query: Optional[str] = None,
    current_user_id: int = Depends(get_current_user_id)
):
    """Obtiene una lista paginada de usuarios con soporte para filtros (requiere autenticación)."""
    result = user_service.obtener_usuarios(skip=skip, limit=limit, rol=rol, estado=estado, query=query)
    return {
        "total": result["total"],
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "limit": limit,
        "data": result["data"]
    }

@router.post("/", response_model=dict)
def create_user(usuario: UsuarioCreate, current_user_id: int = Depends(get_current_user_id)):
    """Registra un nuevo usuario en el sistema (requiere autenticación)."""
    user_id = user_service.crear_usuario(usuario)
    if not user_id:
        raise HTTPException(status_code=400, detail="Error creando usuario")
    return {"message": "Usuario creado exitosamente", "id_usuario": user_id}

@router.get("/{id_usuario}", response_model=UsuarioResponse)
def get_user(id_usuario: int, current_user_id: int = Depends(get_current_user_id)):
    """Obtiene la información detallada de un usuario por su ID (requiere autenticación)."""
    user = user_service.obtener_usuario_por_id(id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{id_usuario}", response_model=UsuarioResponse)
def update_user(id_usuario: int, usuario: UsuarioUpdate, current_user_id: int = Depends(get_current_user_id)):
    """Actualiza la información de un usuario existente (requiere autenticación)."""
    exito = user_service.actualizar_usuario(id_usuario, usuario)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no modificado")
    
    updated_user = user_service.obtener_usuario_por_id(id_usuario)
    return updated_user

@router.delete("/{id_usuario}", response_model=dict)
def delete_user(id_usuario: int, current_user_id: int = Depends(get_current_user_id)):
    """Elimina permanentemente un usuario del sistema (requiere autenticación)."""
    exito = user_service.eliminar_usuario(id_usuario)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}

