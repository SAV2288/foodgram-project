from posts.models import Recipe
from posts.models import Shop_list


def get_ingredients(request):
    """ Формирует список ингредиентов вида: 'ингредиент(ед. изменрения) - количество'. """
    
    recipe_list = Shop_list.objects.filter(user=request.user).values_list("recipe")
    recipe_composition_list = Recipe.objects.filter(id__in=recipe_list).prefetch_related("recipe_composition", "recipe_composition__ingredient")

    # получить список ингредиентов и количество
    ingredients = []
    amount = []

    for p in recipe_composition_list:
        for item in p.recipe_composition.all():
            ingredients.append((item.ingredient.name, item.ingredient.units))
            amount.append(item.amount)

    # Объединить одинаковые ингредиенты(количество суммировать)
    ingredients_set = []
    while ingredients:
        ingreduent = ingredients.pop()
        ingredient_amount = amount.pop()
        ingredients_set.append([ingreduent[0], ingreduent[1], int(ingredient_amount)])
        count_double_ingredient = ingredients.count(ingreduent)
        while count_double_ingredient:
            count_double_ingredient -= 1
            double_ingredient_index = ingredients.index(ingreduent)
            ingredients_set[-1][2] += int(amount[double_ingredient_index])
            ingredients.remove(ingreduent)
            amount.remove(amount[double_ingredient_index])

    ingredients = [ f"{ ingredient[0] } ({ ingredient[1] }) - { ingredient[2] }\n" for ingredient in ingredients_set ]

    return ingredients