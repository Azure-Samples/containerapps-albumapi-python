from pydantic import BaseModel, ConfigDict


class AlbumResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    artist: str
    price: float
    image_url: str