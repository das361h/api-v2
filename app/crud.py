# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def get_recipes_by_ingredients(db: Session, ingredients: List[str]):
    return db.query(models.Recipe).filter(
        models.Recipe.ribs.contains(ingredients)
    ).all()

def get_recipe_by_id(db: Session, rid: str):
    return db.query(models.Recipe).filter(models.Recipe.rid == rid).first()
