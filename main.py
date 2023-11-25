from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json 

# import seed-movies json into an array
with open('./data/seed-movies.json') as f:
    data = json.load(f)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Movie(BaseModel):
    title: str
    year: int
    director: str

@app.get("/movies")
def read_root():
    return data

@app.get("/movies/{movie_id}")
def read_item(movie_id: int, q: Union[str, None] = None):
    if movie_id >= len(data):
        raise HTTPException(status_code=404, detail="Movie not found")
    return { "movie": data[movie_id] }


@app.put("/movies/{movie_id}")
def update_item(movie_id: int, movie: Movie):
    if movie_id >= len(data):
        raise HTTPException(status_code=404, detail="Movie not found")
    data[movie_id] = movie
    return {"movie": movie, "movie_id": movie_id}

@app.post("/movies")
def add_item(movie: Movie):
    data.append(movie)
    return {"movie": movie, "movie_id": len(data)-1}
