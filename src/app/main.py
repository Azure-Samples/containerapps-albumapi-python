from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods="GET",
    allow_headers=["*"]
)

class Album():
    def __init__(self, id, title, artist, price, image_url):
         self.id = id
         self.title = title
         self.artist = artist
         self.price = price
         self.image_url = image_url

albums = [ 
    Album(1, "Sgt Peppers Lonely Hearts Club Band", "The Beatles", 10.99, "https://www.listchallenges.com/f/items/f3b05a20-31ae-4fdf-aebd-d1515af54eea.jpg"),
    Album(2, "Pet Sounds", "The Beach Boys", 13.99, "https://www.listchallenges.com/f/items/fdef1440-e979-455a-90a7-14e77fac79af.jpg"),
    Album(3, "The Beatles: Revolver", "The Beatles", 13.99, "https://www.listchallenges.com/f/items/19ff786d-d7a4-4fdc-bee2-59db8b33370d.jpg"),
    Album(4, "Highway 61 Revisited", "Bob Dylan", 12.99,"https://www.listchallenges.com/f/items/428cf087-6c24-45ad-bf8c-bd3c57ddf444.jpg"),
    Album(5, "Rubber Soul", "The Beatles", 12.99, "https://www.listchallenges.com/f/items/ebc794ef-1491-4672-a007-0081edc1a8ae.jpg"),
    Album(6, "What's Going On", "Marvin Gaye", 14.99, "https://www.listchallenges.com/f/items/e5250d6c-1c15-4617-a943-b27e87e21704.jpg")
]

@app.get("/")
def read_root():
    return {"Azure Container Apps Python Sample API"}


@app.get("/albums")
def get_albums():
    return albums
