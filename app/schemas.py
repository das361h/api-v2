# app/schemas.py
from pydantic import BaseModel
from typing import List, Dict

class RecipeBase(BaseModel):
    rid: str
    rname: str
    ribs: Dict[str, str]
    ringred: Dict[str, str]
    rtype: str
    rserving: int
    rcuisine: str
    roveralltime: str
    rstep: List[str]
    rimage: str

    class Config:
        orm_mode = True
