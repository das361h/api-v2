from fastapi import FastAPI, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import Recipe, Favorite
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for Android access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/search/")
def search_recipes(ingredients: List[str] = Query(...), db: Session = Depends(get_db)):
    user_ingredients_set = set(i.lower() for i in ingredients)
    recipes = db.query(Recipe).all()
    result = []

    for recipe in recipes:
        if recipe.ribs and all(i.lower() in user_ingredients_set for i in recipe.ribs):
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

@app.get("/addfav/")
def add_to_favorites(uid: str, rid: str, db: Session = Depends(get_db)):
    fav = db.query(Favorite).filter(Favorite.userid == uid).first()

    if fav:
        favid_list = fav.favid.split(",") if fav.favid else []
        if rid not in favid_list:
            favid_list.append(rid)
            fav.favid = ",".join(favid_list)
            db.commit()
    else:
        new_fav = Favorite(userid=uid, favid=rid)
        db.add(new_fav)
        db.commit()

    return {"status": "success"}


@app.get("/removefav/")
def remove_from_favorites(uid: str, rid: str, db: Session = Depends(get_db)):
    fav = db.query(Favorite).filter(Favorite.userid == uid).first()

    if fav:
        favid_list = fav.favid.split(",") if fav.favid else []
        if rid in favid_list:
            favid_list.remove(rid)
            fav.favid = ",".join(favid_list)
            db.commit()
            return {"status": "removed"}
        else:
            return {"status": "did not have"}
    else:
        return {"status": "uid not found"}
    
@app.get("/viewfav/")
def view_favorites(uid: str, db: Session = Depends(get_db)):
    fav = db.query(Favorite).filter(Favorite.userid == uid).first()

    if not fav or not fav.favid:
        return []

    rid_list = fav.favid.split(",")
    recipes = db.query(Recipe).filter(Recipe.rid.in_(rid_list)).all()

    result = []
    for recipe in recipes:
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

@app.get("/searchany/")
def search_any(string: str, db: Session = Depends(get_db)):
    keyword = string.lower()
    recipes = db.query(Recipe).all()
    result = []

    for recipe in recipes:
        if (
            keyword in (recipe.rname or "").lower() or
            keyword in (recipe.rtype or "").lower() or
            keyword in (recipe.rcuisine or "").lower() or
            keyword in (recipe.ringred or "").lower() or
            keyword in (recipe.rstep or "").lower()
        ):
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

