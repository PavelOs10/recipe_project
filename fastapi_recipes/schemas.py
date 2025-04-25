from pydantic import BaseModel
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    title: str
    description: str
    ingredients: Optional[str] = None
    steps: str
    preparation_time: int
    category_ids: Optional[List[int]] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    categories: Optional[List[Category]] = None
    author_id: int

    class Config:
        orm_mode = True