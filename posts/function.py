import re

from django.shortcuts import get_list_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count

from posts.models import Tag
from posts.models import Ingredient
from posts.models import Recipe_composition
from posts.models import Recipe_tag
from posts.models import Shop_list

User = get_user_model()


def get_tags(tag_dict, edit=False):
    """ Получение тегов из формы.
    Если форма прошла валидацию вернет объекты,
    если нет, то список тегов """

    tags_list = [tag for tag, value in tag_dict.items() if value]

    if not edit:
        tags_list = Tag.objects.filter(title__in=tags_list)

    return tags_list


def get_ingredients_from_form(request):
    """ Получение списка ингредиентов из формы """
    # получить даные из формы
    nameingredients = request.POST.getlist('nameIngredient')
    unitsingredients = request.POST.getlist('unitsIngredient')
    amount = request.POST.getlist('valueIngredient')

    # обработать данные
    ingredients = []
    for i in range(len(nameingredients)):
        ingredients.append({ "name": nameingredients[i], "units": unitsingredients[i], "amount": amount[i] })

    return ingredients



def get_ingredients(request):
    """ Получение списка объектов ингредиентов для записи в рецепт """

    # получить даные из формы
    ingredients = get_ingredients_from_form(request)
    name_ingredients_list = [ingredient["name"] for ingredient in ingredients]

    # получить список ингредиентов, имеющихся в базе
    ingredients_db = [name[0] for name in Ingredient.objects.filter(name__in=name_ingredients_list).values_list("name")]

    # дописать ноые ингридиенты
    new_ingredient = [ingredient for ingredient in ingredients if ingredient["name"] not in ingredients_db]

    if new_ingredient:
        for ingredient in new_ingredient:
            Ingredient.objects.create(name=ingredient["name"], units=ingredient["units"])

    # получить объекты ингредиентов
    ingredients_object = Ingredient.objects.filter(name__in=name_ingredients_list)

    # Составить список ингредиентов для рецепта
    recipe_ingredients_list = []
    for ingredient in ingredients:
        recipe_ingredients_list.append({ "obj": ingredients_object.get(name=ingredient["name"]), "amount": ingredient["amount"] })

    return recipe_ingredients_list


def remove_data(recipe):
    """ Удаление состава и тегов рецепта.
    (Используется при редактировании рецепта) """
    Recipe_composition.objects.filter(recipe=recipe).delete()
    Recipe_tag.objects.filter(recipe=recipe).delete()


def get_params(request):
    """ Получение параметров, общих для страниц
    - Колличество рецептов в списке покупок
    - Активная страница (для подсвечивания соответствующего пункта меню)
    - Список рецептов в списке покупок
    - Список рецептов в избранном
    - Список авторов, на которых подписан пользователь
    """

    # Получить активную страницу (для подсвечивания соответствующего пункта меню)
    page_activ = (request.META['PATH_INFO']).split("/")[1]

    if request.user.is_authenticated:

        user_params = get_list_or_404(User.objects.prefetch_related("shop_list_recipe_user", "favorites_recipe_user", "follower"), username=request.user)

        # Список рецептов в списке покупок
        shop_list = [item.recipe_id for p in user_params for item in p.shop_list_recipe_user.all()]
        # Список рецептов в избранном
        favorites_list = [item.recipe_id for p in user_params for item in p.favorites_recipe_user.all()]
        # Список авторов, на которых подписан пользователь
        subscriptions_list = [item.author.id for p in user_params for item in p.follower.all()]
        # Колличество рецептов в списке покупок
        shop_list_count = len(shop_list)

        params = {
            "shop_list_count": shop_list_count,
            "page_activ": page_activ,
            "shop_list": shop_list,
            "favorites_list": favorites_list,
            "subscriptions_list": subscriptions_list
        }

    else:
        params = {
            "page_activ": page_activ,
        }

    return params

def get_filter_params(request):
    """ Получение параметров из GET запроса """

    data = ["breakfast", "lunch", "dinner"]

    params = {}
    for item in data:
        params[item] = request.GET.get(item, "")

    return params


def page_filter_params(request):
    """ Управление параметрами фильтрации рецептов в GET запросе """

    params = get_filter_params(request)

    # Формирование дополнительного запроса с параметрами фильтрации
    urlparams = ""
    for item, value in params.items():
        if value == "on":
            urlparams += f"{item}=on&"

    page_filter_params = {"params": params, "urlparams": urlparams}

    return page_filter_params