from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import Recipe
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins for development (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/search/")
def search_recipes(ingredients: List[str] = Query(...), db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()
    result = []
    for recipe in recipes:
        if recipe.ribs:
            if all(ing.lower() in [i.lower() for i in recipe.ribs] for ing in ingredients):
                result.append({
                    "rid": recipe.rid,
                    "rname": recipe.rname,
                    "rtype": recipe.rtype,
                    "rserving": recipe.rserving,
                    "rcuisine": recipe.rcuisine,
                    "roveralltime": recipe.roveralltime,
                    "ringred": recipe.ringred,
                    "rstep": recipe.rstep,
                    "rimage": recipe.rimage,
                })
    return result
