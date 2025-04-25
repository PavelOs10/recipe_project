from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import models, schemas

app = FastAPI()

@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

@app.get("/recipes/by_title/{title}", response_model=schemas.Recipe)
def read_recipe_by_title(title: str, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.title == title).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe with this title not found")
    return db_recipe

@app.get("/recipes/by_ingredient/{ingredient}", response_model=List[schemas.Recipe])
def read_recipes_by_ingredient(ingredient: str, db: Session = Depends(get_db)):
    db_recipes = db.query(models.Recipe).filter(models.Recipe.ingredients.like(f"%{ingredient}%")).all()
    return db_recipes

@app.get("/categories/{category_id}/recipes", response_model=List[schemas.Recipe])
def read_recipes_by_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.models.Category).filter(models.models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category.recipes

@app.get("/recipes/", response_model=List[schemas.Recipe])
def read_all_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = db.query(models.Recipe).offset(skip).limit(limit).all()
    return recipes

@app.get("/categories/", response_model=List[schemas.Category])
def read_all_categories(db: Session = Depends(get_db)):
    categories = db.query(models.models.Category).all()
    return categories

@app.post("/recipes/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = models.Recipe(
        title=recipe.title,
        description=recipe.description,
        ingredients=recipe.ingredients,
        steps=recipe.steps,
        preparation_time=recipe.preparation_time,
        author_id=1,
    )
    if recipe.category_ids:
        db_recipe.categories = db.query(models.models.Category).filter(models.models.Category.id.in_(recipe.category_ids)).all()
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    db_category = models.models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.patch("/recipes/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(recipe_id: int, recipe_update: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    update_data = recipe_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_recipe, key, value)
    if recipe_update.category_ids is not None:
        db_recipe.categories = db.query(models.models.Category).filter(models.models.Category.id.in_(recipe_update.category_ids)).all()
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@app.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
def full_update_recipe(recipe_id: int, recipe_update: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    update_data = recipe_update.dict()
    for key, value in update_data.items():
        setattr(db_recipe, key, value)
    if recipe_update.category_ids is not None:
        db_recipe.categories = db.query(models.models.Category).filter(models.models.Category.id.in_(recipe_update.category_ids)).all()
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe