from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Tag, Ingredient
from django.urls import reverse
from django.contrib import messages
from .forms import RecipeFrom, IngredientForm, IngredientEditForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator


def recipe_list(request):
    recipes = Recipe.objects.order_by('-id')
    tag = request.GET.get('tag')
    if tag:
        recipes = recipes.filter(tags__title=tag)
    paginator = Paginator(recipes, 1)
    page_number = request.GET.get("page")
    page_qs = paginator.get_page(page_number)
    is_active = True if page_qs.number == page_number else False

    context = {
        'object_list': page_qs,
        'is_active': is_active
    }
    return render(request,'recipe/index.html', context)


def my_recipe_list(request):
    recipes = Recipe.objects.filter(author_id=request.user.id).order_by('-id')
    tag = request.GET.get('tag')
    if tag:
        recipes = recipes.filter(tags__title=tag)
    context = {
        'object_list': recipes
    }
    return render(request, 'recipe/index.html', context)


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    is_author_lookup = Q(is_active=True)
    if request.user == recipe.author:
        is_author_lookup = Q()
    ingredients = Ingredient.objects.filter(Q(recipe_id=recipe.id) & is_author_lookup)
    is_author = request.user == recipe.author
    context = {
        'object': recipe,
        'ingredients': ingredients,
        'is_author': is_author
    }
    return render(request, 'recipe/detail.html', context)


def recipe_create(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You should login first.')
        reverse_url = reverse('auth:login') + '?next=' + request.path
        return redirect(reverse_url)
    form = RecipeFrom()
    if request.method == 'POST':
        form = RecipeFrom(request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author_id = request.user.id
            obj.save()
            form.save_m2m()
            detail_url = reverse('recipe:detail', args=[obj.slug])
            return redirect(detail_url)
    context = {
        "form": form
    }
    return render(request, 'recipe/create.html', context)


def recipe_update(request, slug):
    instance = get_object_or_404(Recipe, slug=slug)
    form = RecipeFrom(instance=instance)
    if request.method == 'POST':
        form = RecipeFrom(data=request.POST, files=request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            detail_url = reverse('recipe:detail', args=[instance.slug])
            return redirect(detail_url)

    context = {
        'form': form,
        'header': 'header'
    }
    return render(request, 'recipe/create.html', context)


def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.method == 'POST':
        if not request.user.id == recipe.author_id:
            messages.warning(request, 'You have no enough permission to delete.')
            return redirect(reverse('recipe:detail', args=[recipe.slug]))
        recipe.delete()
        return redirect('recipe:list')
    context = {
        'object': recipe
    }
    return render(request, 'recipe/delete.html', context)


def recipe_ingredient_create(request, slug):
    form = IngredientForm()
    recipe = get_object_or_404(Recipe, slug=slug)
    reverse_url = reverse('recipe:detail', args=[recipe.slug])
    if recipe.author == request.user:
        messages.error(request, "You have no enough permissions")
        return redirect(reverse_url)
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.recipe = recipe
            obj.save()
            messages.success(request, f'You created new ingredient "{obj.title}".')
            return redirect(reverse_url)
    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'recipe/recipe_ingredient_create.html', context)


def recipe_ingredient_edit(request, slug, pk, *args, **kwargs):
    recipe = get_object_or_404(Recipe, slug=slug)
    reverse_url = reverse('recipe:detail', args=[slug])
    instance = get_object_or_404(Ingredient, id=pk)
    if instance not in recipe.ingredient_set.all():         # modelname_set
        raise ObjectDoesNotExist(f'{instance.title} doe not exist in {recipe.title} recipe')
    if recipe.author == request.user:
        messages.error(request, "You have no enough permissions")
        return redirect(reverse_url)
    form = IngredientEditForm(instance=instance)
    if request.method == "POST":
        form = IngredientEditForm(data=request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'You edit new ingredient "{obj.title}".')
            return redirect(reverse_url)
    context = {
        'form': form,
        'recipe': recipe,
        'title': 'Change ingredient belong to'

    }
    return render(request, 'recipe/recipe_ingredient_create.html', context)


def recipe_ingredient_delete(request, *args, **kwargs):
    recipe = get_object_or_404(Recipe, slug=kwargs['slug'])
    instance = get_object_or_404(Ingredient, id=kwargs['pk'])
    reverse_url = reverse('recipe:detail', args=[kwargs['slug']])
    if instance not in recipe.ingredient_set.all():         # modelname_set
        raise ObjectDoesNotExist(f'{instance.title} doe not exist in {recipe.title} recipe')
    if recipe.author == request.user:
        messages.error(request, "You have no enough permissions")
        return redirect(reverse_url)
    if request.method == "POST":
        instance.delete()
        messages.error(request, f'"{instance.title}" delete')
        return redirect(reverse_url)
    context = {
        'object': instance
    }
    return render(request, 'recipe/ingredient_delete.html', context)