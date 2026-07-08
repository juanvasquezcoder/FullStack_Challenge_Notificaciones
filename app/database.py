from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# check_same_thread=False es necesario SOLO para SQLite,
# porque por defecto SQLite no permite compartir la conexión entre threads,
# y FastAPI maneja requests en threads distintos.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()