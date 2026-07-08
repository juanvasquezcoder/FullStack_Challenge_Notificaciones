from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.routers import auth, notifications, pages, admin, channels
import app.models  # importa User y Notification para que create_all los detecte

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Notificaciones")

app.include_router(auth.router)
app.include_router(notifications.router)
app.include_router(pages.router)
app.include_router(admin.router)
app.include_router(channels.router)

# app.mount("/registro", StaticFiles(directory="app/static/", html=True), name="static")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return {"message": "API funcionando"}