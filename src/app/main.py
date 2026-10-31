import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Album
from app.schemas import AlbumResponse


app = FastAPI(
    title="Album API",
    description="Album API backed by SQLAlchemy and Alembic",
    version="1.0.0"
)


# Configure CORS through environment variables.
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"message": "Album API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/albums", response_model=list[AlbumResponse])
def get_albums(db: Session = Depends(get_db)):
    statement = select(Album).order_by(Album.id)

    albums = db.scalars(statement).all()

    return albums
