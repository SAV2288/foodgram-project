import os
from django.http import FileResponse

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse

from api import function
from posts.models import Follow
from posts.models import Ingredient
from posts.models import Favorites
from posts.models import Recipe
from posts.models import Shop_list




User = get_user_model()

@login_required
def profile_follow(request, username):
    """ Подписаться на автора """

    author = get_object_or_404(User, username=username)
    
    if request.user != author:
        follow = Follow.objects.get_or_create(user=request.user, author=author)
        if follow[1]:
            return JsonResponse({"status": "true", "message": f"Вы подписались на автора {author.first_name} {author.last_name}"}, status=200, safe=False)
        else:
            return JsonResponse({"status": "false", "message": f"Вы уже подписаны на автора {author.first_name} {author.last_name}"}, status=400, safe=False)


@login_required
def profile_unfollow(request, username):
    """ Отписаться от автора """

    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=request.user, author=author).delete()
    return JsonResponse({"status": "true", "message": f"Автор {author.first_name} {author.last_name} удален из подписки"}, status=200, safe=False)


@login_required
def recipe_favorite(request, recipe_id):
    """ Добавить рецепт в избранное """

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        favorite = Favorites.objects.get_or_create(user=request.user, recipe=recipe)
        if favorite[1]:
            result = {"status": "true", "message": f"Рецепт '{recipe.title}' добавлен в избранное"}
            status = 200
        else:
            result = {"status": "false", "message": f"Рецепт '{recipe.title}' уже в избранном"}
            status = 400
    else:
        result = {"status": "false", "message": f"Нельзя добавить в избранное свой рецепт"}
        status = 400
    return JsonResponse(result, status=status, safe=False)


@login_required
def recipe_unfavorite(request, recipe_id):
    """ Удалить рецепт из избранного """

    recipe = get_object_or_404(Recipe, id=recipe_id )
    favorite = Favorites.objects.filter(user=request.user, recipe=recipe).delete()
    return JsonResponse({"status": "true", "message": f"Рецепт '{recipe.title}' удален из избранного"}, status=200, safe=False)


@login_required
def get_ingredients(request, name):
    """ Получить список ингредиентов. Фильтрует по названию """

    ingreduents = Ingredient.objects.filter(name__startswith=name).values("name", "units")
    results = [{"name": ingredient["name"], "units":ingredient["units"]} for ingredient in ingreduents ]
    return JsonResponse({"results": results}, status=200, safe=False)


@login_required
def recipe_to_shop_list(request, recipe_id):
    """ Добавить рецепт в список покупок """

    recipe = get_object_or_404(Recipe, id=recipe_id)
    add_to_shop_list = Shop_list.objects.get_or_create(user = request.user, recipe=recipe)
    if add_to_shop_list[1]:
        return JsonResponse({"status": "true", "message": f"Рецепт '{recipe.title}' добавлен в список покупок"}, status=200, safe=False)
    return JsonResponse({"status": "false", "message": "Рецепт уже есть в списке покупок"}, status=400, safe=False)


@login_required
def recipe_remove_in_shop_list(request, recipe_id):
    """ Удалить рецепт из списка покупок """

    recipe = get_object_or_404(Recipe, id=recipe_id)
    remove_recipe = Shop_list.objects.filter(user=request.user, recipe=recipe).delete()
    return JsonResponse({"status": "true", "message": f"Рецепт '{recipe.title}' удален из списока покупок"}, status=200, safe=False)


@login_required
def get_shop_list_count(request):
    """ Получить колличество рецептов в списке покупок """

    shop_list = Shop_list.objects.filter(user=request.user).count()
    return JsonResponse({"results": shop_list}, status=200, safe=False)


@login_required
def download_shop_list(request):
    """ Скачать файл со списком ингредиентов для рецептов из списка покупок """

    ingredients = function.get_ingredients(request)

    try:
        with open(f"temp_file/Shop_list({ request.user.username }).txt", "w") as f:
            f.write("FoodGram | Список покупок\n\n")
            f.writelines(ingredients)
        response = FileResponse(open(f"temp_file/Shop_list({ request.user.username }).txt", "rb"))
        return response
    finally:
        os.remove(f"temp_file/Shop_list({ request.user.username }).txt")
