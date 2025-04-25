from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Recipe, Category
from .forms import RecipeForm, UserRegistrationForm, LoginForm
from django.db.models import Q
from django.contrib.auth.models import User

def home(request):
    random_recipes = Recipe.objects.order_by('?')[:5]
    context = {'random_recipes': random_recipes}
    return render(request, 'recipes_app/recipe_list.html', context)

def all_recipes(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    context = {'recipes': recipes}
    return render(request, 'recipes_app/all_recipes.html', context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {'recipe': recipe}
    return render(request, 'recipes_app/recipe_detail.html', context)

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    context = {'form': form}
    return render(request, 'recipes_app/create_recipe.html', context)

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            form.save_m2m()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    context = {'form': form, 'recipe': recipe}
    return render(request, 'recipes_app/create_recipe.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def search_recipes(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Recipe.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(ingredients__icontains=query)
        ).order_by('-created_at')
    context = {'query': query, 'results': results}
    return render(request, 'recipes_app/search_results.html', context)

def recipes_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    recipes = Recipe.objects.filter(categories=category).order_by('-created_at')
    context = {'category': category, 'recipes': recipes}
    return render(request, 'recipes_app/recipes_by_category.html', context)