from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    title = Column(String)
    cuisine = Column(String)
    difficulty = Column(String)
    data_json = Column(JSON)