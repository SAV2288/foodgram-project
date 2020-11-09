from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new_post/", views.new_post, name="new_post"),
    path("follow/", views.follow_index, name="follow_index"),
    path("favorites/", views.favorites_index, name="favorites_index"),
    path(
        "recipes/<str:username>/",
        views.author_recipes,
        name="author_recipes"
        ),
    path("<str:username>/<int:post_id>/", views.post_view, name="post"),
    path(
        "<str:username>/<int:post_id>/edit/",
        views.post_edit,
        name="post_edit"
        ),
    path("shop_list/", views.shop_list_index, name="shop_list"),
]
