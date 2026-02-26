import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Si corres la app en Windows, usa localhost. 
# Si la corres dentro de Docker, el host será 'db'.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://usuario_devops:password_seguro@localhost:5432/notas_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para inyectar la sesión de DB en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()