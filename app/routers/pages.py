from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["pages"])
HTML_DIR = "app/static/html"

@router.get("/")
def serve_index():
    return FileResponse(f"{HTML_DIR}/index.html")

@router.get("/login")
def serve_login():
    return FileResponse(f"{HTML_DIR}/login.html")

@router.get("/registro")
def serve_register():
    return FileResponse(f"{HTML_DIR}/register.html")


@router.get("/me")
def serve_me():
    return FileResponse(f"{HTML_DIR}/me.html")


@router.get("/notificaciones")
def serve_notifications():
    return FileResponse(f"{HTML_DIR}/notifications.html")