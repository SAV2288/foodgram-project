from django.urls import path
from . import views


urlpatterns = [
    path("<username>/follow", views.profile_follow, name="profile_follow"),
    path("<username>/unfollow", views.profile_unfollow, name="profile_unfollow"),
    path("<recipe_id>/favorite", views.recipe_favorite, name="recipe_favorite"),
    path("<recipe_id>/unfavorite", views.recipe_unfavorite, name="recipe_unfavorite"),
    path("ingredients/<name>", views.get_ingredients, name="recipe_unfavorite"),
    path("<recipe_id>/shop_list", views.recipe_to_shop_list, name="recipe_shop_list"),
    path("<recipe_id>/remove_in_shop_list", views.recipe_remove_in_shop_list, name="recipe_remove_in_shop_list"),
    path("shop_list_count", views.get_shop_list_count, name="get_shop_list_count"),
    path("shop_list", views.download_shop_list, name="download_shop_list"),
]