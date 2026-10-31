from sqlalchemy import select

from app.database import Base, engine, SessionLocal
from app.models import Album


def initialize_database():

    with SessionLocal() as db:
        # Check whether albums are already stored.
        existing_album = db.scalar(
            select(Album.id).limit(1)
        )

        if existing_album is not None:
            print("Albums already exist. Skipping seed.")
            return

        # Insert our original sample albums.
        albums = [
            Album(
                id=1,
                title="You, Me and an App Id",
                artist="Daprize",
                price=10.99,
                image_url="https://aka.ms/albums-daprlogo"
            ),
            Album(
                id=2,
                title="Seven Revision Army",
                artist="The Blue-Green Stripes",
                price=13.99,
                image_url="https://aka.ms/albums-containerappslogo"
            ),
            Album(
                id=3,
                title="Scale It Up",
                artist="KEDA Club",
                price=13.99,
                image_url="https://aka.ms/albums-kedalogo"
            ),
            Album(
                id=4,
                title="Lost in Translation",
                artist="MegaDNS",
                price=12.99,
                image_url="https://aka.ms/albums-envoylogo"
            ),
            Album(
                id=5,
                title="Lock Down Your Love",
                artist="V is for VNET",
                price=12.99,
                image_url="https://aka.ms/albums-vnetlogo"
            ),
            Album(
                id=6,
                title="Sweet Container O' Mine",
                artist="Guns N Probeses",
                price=14.99,
                image_url="https://aka.ms/albums-containerappslogo"
            )
        ]

        db.add_all(albums)
        db.commit()

        print(f"Successfully inserted {len(albums)} albums.")


if __name__ == "__main__":
    initialize_database()