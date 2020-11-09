from django.shortcuts import get_list_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


def get_params(request):
    """ Получение параметров, общих для страниц
    - Колличество рецептов в списке покупок
    - Активная страница (для подсвечивания соответствующего пункта меню)
    - Список рецептов в списке покупок
    - Список рецептов в избранном
    - Список авторов, на которых подписан пользователь
    """

    # Получить активную страницу
    # (для подсвечивания соответствующего пункта меню)
    page_activ = (request.META['PATH_INFO']).split("/")[1]

    if request.user.is_authenticated:

        user_params = get_list_or_404(
            User.objects.prefetch_related(
                "shop_list_recipe_user",
                "favorites_recipe_user",
                "follower"
            ),
            username=request.user
        )

        # Список рецептов в списке покупок
        shop_list = [item.recipe_id for p in user_params
                     for item in p.shop_list_recipe_user.all()]
        # Список рецептов в избранном
        favorites_list = [item.recipe_id for p in user_params
                          for item in p.favorites_recipe_user.all()]
        # Список авторов, на которых подписан пользователь
        subscriptions_list = [item.author.id for p in user_params
                              for item in p.follower.all()]
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
