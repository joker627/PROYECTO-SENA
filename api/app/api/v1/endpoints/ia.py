"""Endpoint de IA: traducción de lenguaje de señas."""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.schemas.ia import TraduccionResponse
from app.services.ia import traducir_video

router = APIRouter()


@router.post("/traducir-video", response_model=TraduccionResponse)
async def traducir_video_endpoint(file: UploadFile = File(...)):
    """Recibe un video y retorna la seña detectada."""

    # Validar tipo de archivo
    tipos_permitidos = ["video/mp4", "video/avi", "video/webm", "video/quicktime"]
    if file.content_type not in tipos_permitidos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no permitido: {file.content_type}. "
                   f"Tipos aceptados: {', '.join(tipos_permitidos)}"
        )

    # Leer contenido del video
    video_bytes = await file.read()

    if len(video_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo de video está vacío"
        )

    # Procesar con el servicio de IA
    resultado = traducir_video(video_bytes)

    return resultado
