# app/models.py
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.dialects.mysql import JSON
from .database import Base

class Recipe(Base):
    __tablename__ = "recipedb"

    rid = Column(String(4), primary_key=True, index=True)
    rname = Column(Text)
    ribs = Column(JSON)
    ringred = Column(JSON)
    rtype = Column(Text)
    rserving = Column(Integer)
    rcuisine = Column(Text)
    roveralltime = Column(Text)
    rstep = Column(JSON)
    rimage = Column(Text)
