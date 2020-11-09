from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from posts import function
from posts.models import Recipe
from posts.models import Recipe_composition
from posts.models import Follow
from posts.models import Favorites
from posts.models import Shop_list
from posts.models import Recipe_tag
from posts.forms import NewRecipe
from posts.forms import NewRecipeComp
from posts.forms import TagForm
from posts.filters import TagFilter


User = get_user_model()


def index(request):
    tag_filter = TagFilter(
        request.GET,
        queryset=Recipe.objects.all()
        .prefetch_related("tag_recipe").order_by("-pub_date"))

    page_filter_params = function.page_filter_params(request)

    paginator = Paginator(tag_filter.qs, 9)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {
                      "page": page,
                      "paginator": paginator,
                      "tag_filter": tag_filter,
                      "page_filter_params": page_filter_params
                  })


@login_required
def new_post(request):
    """ Страница создания нового рецепта """

    recipe_form = NewRecipe(request.POST or None, files=request.FILES or None)
    recipe_comp_form = NewRecipeComp(request.POST or None)
    tag_form = TagForm(request.POST or None)

    context = {
                "recipe_form": recipe_form,
                "recipe_comp_form": recipe_comp_form,
                "tag_form": tag_form
        }

    if request.method == "POST":

        if recipe_form.is_valid() and tag_form.is_valid():

            ingredients = function.get_ingredients(request)

            if ingredients:
                recipe = recipe_form.save(commit=False)
                recipe.author = request.user
                recipe.save()

                for ingredient in ingredients:
                    Recipe_composition.objects.create(
                        ingredient=ingredient["obj"],
                        amount=ingredient["amount"],
                        recipe=recipe
                    )

                tags = function.get_tags(tag_form.cleaned_data)
                for tag in tags:
                    Recipe_tag.objects.create(tag=tag, recipe=recipe)

                return redirect("/")

        else:
            ingredients = function.get_ingredients_from_form(request)
            context["ingredients"] = ingredients

    return render(request, "new_post.html", context)


def author_recipes(request, username):
    """ Страница с рецептами определенного автора """

    author = get_object_or_404(User, username=username)
    tag_filter = TagFilter(
        request.GET,
        queryset=Recipe.objects.filter(author=author)
        .prefetch_related("tag_recipe").order_by("-pub_date"))

    page_filter_params = function.page_filter_params(request)

    paginator = Paginator(tag_filter.qs, 9)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "profile.html",
                  {
                      "page": page,
                      "paginator": paginator,
                      "author": author,
                      "tag_filter": tag_filter,
                      "page_filter_params": page_filter_params
                  })


def post_view(request, username, post_id):
    """ Страница рецепта """

    author = get_object_or_404(User, username=username)
    post = get_object_or_404(
        Recipe.objects.prefetch_related("tag_recipe"),
        pk=post_id,
        author=author
    )
    ingredients = Recipe_composition.objects.filter(recipe=post)\
        .select_related("ingredient")

    return render(request, "post.html",
                  {
                      "post": post,
                      "ingredients": ingredients
                  })


@login_required
def post_edit(request, username, post_id):
    """ Страница редактирования рецепта """

    user = get_object_or_404(User, username=username)
    recipe = get_object_or_404(
            Recipe.objects.prefetch_related(
                "recipe_composition__ingredient",
                "tag_recipe__tag"
                ),
            pk=post_id,
            author=user
        )

    recipe_form = NewRecipe(
        request.POST or None, files=request.FILES
        or None, instance=recipe
    )
    recipe_comp_form = NewRecipeComp(request.POST or None)
    tag_form = TagForm(request.POST or None)

    tag_active = [item.tag.title for item in recipe.tag_recipe.all()]
    ingredients = [
        {
            "name": item.ingredient.name,
            "units": item.ingredient.units,
            "amount": item.amount
        }
        for item in recipe.recipe_composition.all()
    ]

    context = {
                "recipe_form": recipe_form,
                "recipe_comp_form": recipe_comp_form,
                "tag_form": tag_form,
                "ingredients": ingredients,
                "tag_active": tag_active,
                "edit": True,
                "id": recipe.id
        }

    if request.method == "POST":
        if recipe_form.is_valid() and tag_form.is_valid():
            ingredients = function.get_ingredients(request)
            if ingredients:
                recipe = recipe_form.save(commit=False)
                recipe.author = request.user
                recipe.save()

                function.remove_data(recipe)

                for ingredient in ingredients:
                    Recipe_composition.objects.create(
                        ingredient=ingredient["obj"],
                        amount=ingredient["amount"],
                        recipe=recipe
                    )

                tags = function.get_tags(tag_form.cleaned_data)
                for tag in tags:
                    Recipe_tag.objects.create(tag=tag, recipe=recipe)
                # Выход, если редактирование прошло успешно
                return redirect("/")

        tag_active = function.get_tags(tag_form.cleaned_data, edit=True)
        ingredients = function.get_ingredients_from_form(request)

        return render(request, "new_post.html", context)
    return render(request, "new_post.html", context)


@login_required
def follow_index(request):
    """ Страница подписок на авторов """

    following = Follow.objects.filter(user=request.user).values_list("author")
    author_list = User.objects.filter(id__in=following).all()\
        .prefetch_related("recipes").annotate(recipe_count=Count("recipes"))

    paginator = Paginator(author_list, 9)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html",
                  {
                      "page": page,
                      "paginator": paginator
                  })


@login_required
def favorites_index(request):
    """ Страница избранных рецептов """

    recipe_list = Favorites.objects.filter(user=request.user)\
        .values_list("recipe")
    tag_filter = TagFilter(
        request.GET,
        queryset=Recipe.objects.filter(id__in=recipe_list)
        .prefetch_related("tag_recipe").order_by("-pub_date")
    )

    page_filter_params = function.page_filter_params(request)

    paginator = Paginator(tag_filter.qs, 9)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "favorites.html",
                  {
                      "page": page,
                      "paginator": paginator,
                      "tag_filter": tag_filter,
                      "page_filter_params": page_filter_params
                  })


@login_required
def shop_list_index(request):
    """ Страница с рецептами из списка покупок """

    recipe_list = Shop_list.objects.filter(user=request.user)\
        .select_related("recipe")
    # params = function.get_params(request)
    return render(request, "shop_list.html",
                  {
                      "recipe_list": recipe_list
                  })
