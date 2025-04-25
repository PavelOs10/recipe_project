from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.all_recipes, name='all_recipes'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('recipe/edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('search/', views.search_recipes, name='search_recipes'),
    path('category/<int:category_id>/', views.recipes_by_category, name='recipes_by_category'),
]