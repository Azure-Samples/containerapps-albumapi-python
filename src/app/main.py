import os

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
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


@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    # /health answers as soon as the process is listening, which is what a
    # liveness probe wants. Readiness has to keep failing while the database
    # is still unreachable, otherwise the ingress routes traffic to a replica
    # that cannot serve /albums yet.
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="database unavailable"
        ) from exc

    return {"status": "ready"}


@app.get("/albums", response_model=list[AlbumResponse])
def get_albums(db: Session = Depends(get_db)):
    statement = select(Album).order_by(Album.id)

    albums = db.scalars(statement).all()

    return albums
