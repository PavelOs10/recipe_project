from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

recipe_category_association = Table(
    'recipes_app_recipe_categories', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes_app_recipe.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('recipes_app_category.id'), primary_key=True)
)

class Recipe(Base):
    __tablename__ = "recipes_app_recipe"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    ingredients = Column(String)
    steps = Column(String)
    preparation_time = Column(Integer)
    author_id = Column(Integer, ForeignKey("auth_user.id"))
    categories = relationship("Category", secondary=recipe_category_association)

class Category(Base):
    __tablename__ = "recipes_app_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    recipes = relationship("Recipe", secondary=recipe_category_association, back_populates="categories")