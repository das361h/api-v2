# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/recipes/", response_model=List[schemas.RecipeBase])
def read_recipes(ingredients: List[str], db: Session = Depends(get_db)):
    recipes = crud.get_recipes_by_ingredients(db, ingredients)
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found")
    return recipes

@app.get("/recipes/{rid}", response_model=schemas.RecipeBase)
def read_recipe(rid: str, db: Session = Depends(get_db)):
    recipe = crud.get_recipe_by_id(db, rid)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
