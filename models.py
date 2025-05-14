from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Integer, JSON

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipedb"

    rid = Column(String(4), primary_key=True)
    rname = Column(Text)
    ribs = Column(JSON)
    ringred = Column(JSON)
    rtype = Column(Text)
    rserving = Column(Integer)
    rcuisine = Column(Text)
    roveralltime = Column(Text)
    rstep = Column(JSON)
    rimage = Column(Text)
