from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

# Importamos nuestros módulos locales
from . import models, database

# Crea las tablas en PostgreSQL automáticamente al iniciar
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="DevOps Notes API")

# --- ESQUEMAS DE PYDANTIC (Validación de Datos) ---

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    sentiment: Optional[str] = None

    class Config:
        from_attributes = True

# --- ENDPOINTS (Lógica de Negocio) ---

@app.get("/", tags=["General"])
def read_root():
    return {"message": "API de Notas DevOps funcionando", "db_status": "Connected"}

@app.post("/notes", response_model=NoteResponse, tags=["Notes"])
def create_note(note: NoteCreate, db: Session = Depends(database.get_db)):
    # Lógica de mediana complejidad: Análisis de sentimiento simple
    content_lower = note.content.lower()
    if any(word in content_lower for word in ["bueno", "genial", "excelente", "feliz"]):
        sentiment_result = "Positivo"
    elif any(word in content_lower for word in ["malo", "error", "fallo", "triste"]):
        sentiment_result = "Negativo"
    else:
        sentiment_result = "Neutral"

    # Crear el objeto para la base de datos
    db_note = models.Note(
        title=note.title, 
        content=note.content, 
        sentiment=sentiment_result
    )
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/notes", response_model=List[NoteResponse], tags=["Notes"])
def read_notes(db: Session = Depends(database.get_db)):
    return db.query(models.Note).all()