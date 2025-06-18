from fastapi import FastAPI, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import SessionLocal
from models import Recipe, Favorite
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RecipeUpload(BaseModel):
    rname: str
    rtype: str
    rserving: int
    rcuisine: str
    roveralltime: str
    ringred: List[str]
    rstep: List[str]
    verified: str
    tts: str
    rcal: int
    rfat: int
    rprot: int
    rcarb: int
    rsod: int
    rchol: int

#rcal: Optional[int] = 0
#rfat: Optional[int] = 0
    #rprot: Optional[int] = 0
    #rcarb: Optional[int] = 0
    #rsod: Optional[int] = 0
    #rchol: Optional[int] = 0

@app.post("/upload/")
def upload_recipe(data: RecipeUpload, db: Session = Depends(get_db)):
    recipe = Recipe(
        rname=data.rname,
        rtype=data.rtype,
        rserving=data.rserving,
        rcuisine=data.rcuisine,
        roveralltime=data.roveralltime,
        ringred=data.ringred,
        rstep=data.rstep,
        verified=data.verified,
        tts=data.tts,
        rcal=data.rcal,
        rfat=data.rfat,
        rprot=data.rprot,
        rcarb=data.rcarb,
        rsod=data.rsod,
        rchol=data.rchol,
        rimage=None
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return {"rid": recipe.rid}

@app.get("/updateimage/")
def update_image(rid: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.rid == rid).first()
    filename = f"{rid:05d}.jpg"
    recipe.rimage = "https://raw.githubusercontent.com/das361h/api-v2/refs/heads/main/image/"+filename
    db.commit()
    return {"status": "image dets updated", "rimage": filename}


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
                "verified": recipe.verified,
                "tts": recipe.tts,
                "rcal": recipe.rcal,
                "rfat": recipe.rfat,
                "rprot": recipe.rprot,
                "rcarb": recipe.rcarb,
                "rsod": recipe.rsod,
                "rchol": recipe.rsod,
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
            "verified": recipe.verified,
            "tts": recipe.tts,
            "rcal": recipe.rcal,
            "rfat": recipe.rfat,
            "rprot": recipe.rprot,
            "rcarb": recipe.rcarb,
            "rsod": recipe.rsod,
            "rchol": recipe.rsod,
        })

    return result

@app.get("/searchany/")
def search_any(string: str, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()
    result = []

    if not string or string.strip() == "":
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
                "verified": recipe.verified,
                "tts": recipe.tts,
                "rcal": recipe.rcal,
                "rfat": recipe.rfat,
                "rprot": recipe.rprot,
                "rcarb": recipe.rcarb,
                "rsod": recipe.rsod,
                "rchol": recipe.rsod,
            })
        return result

    keyword = string.lower()

    for recipe in recipes:
        # convert JSON list to string for searching
        ringred_text = " ".join(recipe.ringred) if isinstance(recipe.ringred, list) else str(recipe.ringred)
        rstep_text = " ".join(recipe.rstep) if isinstance(recipe.rstep, list) else str(recipe.rstep)

        if (
            keyword in (recipe.rname or "").lower() or
            keyword in (recipe.rtype or "").lower() or
            keyword in (recipe.rcuisine or "").lower() or
            keyword in ringred_text.lower() or
            keyword in rstep_text.lower()
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
                "verified": recipe.verified,
                "tts": recipe.tts,
                "rcal": recipe.rcal,
                "rfat": recipe.rfat,
                "rprot": recipe.rprot,
                "rcarb": recipe.rcarb,
                "rsod": recipe.rsod,
                "rchol": recipe.rsod,
            })

    return result

@app.get("/deleteuser/")
def delete_user_favorites(user: str, db: Session = Depends(get_db)):
    fav_entry = db.query(Favorite).filter(Favorite.userid == user).first()
    db.delete(fav_entry)
    db.commit()


@app.get("/servings/")
def search_by_serving(amount: int, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).filter(Recipe.rserving >= amount).all()
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
                "verified": recipe.verified,
                "tts": recipe.tts,
                "rcal": recipe.rcal,
                "rfat": recipe.rfat,
                "rprot": recipe.rprot,
                "rcarb": recipe.rcarb,
                "rsod": recipe.rsod,
                "rchol": recipe.rsod,
        })

    return result

@app.get("/cuisine/")
def search_by_cuisine(type: str, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).filter(Recipe.rcuisine.ilike(f"%{type}%")).all()
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
                "verified": recipe.verified,
                "tts": recipe.tts,
                "rcal": recipe.rcal,
                "rfat": recipe.rfat,
                "rprot": recipe.rprot,
                "rcarb": recipe.rcarb,
                "rsod": recipe.rsod,
                "rchol": recipe.rsod,
        })

    return result

@app.get("/type/")
def search_by_type(type: str, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).filter(Recipe.rtype.ilike(f"%{type}%")).all()
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
                "verified": recipe.verified,
                "tts": recipe.tts,
                "rcal": recipe.rcal,
                "rfat": recipe.rfat,
                "rprot": recipe.rprot,
                "rcarb": recipe.rcarb,
                "rsod": recipe.rsod,
                "rchol": recipe.rsod,
        })

    return result

@app.get("/Between/")
def get_between(nutrition: str, value1: float, value2: float, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).filter(getattr(Recipe, nutrition).between(value1, value2)).all()
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
                "verified": recipe.verified,
                "tts": recipe.tts,
                "rcal": recipe.rcal,
                "rfat": recipe.rfat,
                "rprot": recipe.rprot,
                "rcarb": recipe.rcarb,
                "rsod": recipe.rsod,
                "rchol": recipe.rsod,
        })

    return result

@app.get("/Maximum/")
def get_between(nutrition: str, value1: float, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).filter(getattr(Recipe, nutrition) <= value1).all()
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
                "verified": recipe.verified,
                "tts": recipe.tts,
                "rcal": recipe.rcal,
                "rfat": recipe.rfat,
                "rprot": recipe.rprot,
                "rcarb": recipe.rcarb,
                "rsod": recipe.rsod,
                "rchol": recipe.rsod,
        })

    return result

@app.get("/Minimum/")
def get_between(nutrition: str, value1: float, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).filter(getattr(Recipe, nutrition) >= value1).all()
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
                "verified": recipe.verified,
                "tts": recipe.tts,
                "rcal": recipe.rcal,
                "rfat": recipe.rfat,
                "rprot": recipe.rprot,
                "rcarb": recipe.rcarb,
                "rsod": recipe.rsod,
                "rchol": recipe.rsod,
        })

    return result