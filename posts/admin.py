from django.db.models import Count
from django.contrib import admin

from posts.models import Recipe
from posts.models import Ingredient
from posts.models import Recipe_composition
from posts.models import Tag
from posts.models import Recipe_tag
from posts.models import Follow
from posts.models import Favorites
from posts.models import Shop_list


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ("favorites_count",)
    list_display = ("title", "author",) 
    list_filter = ("title", "author", "tag_recipe__tag",)
    empty_value_display = "-пусто-"


    def get_queryset(self, request):
        qs = super(RecipeAdmin, self).get_queryset(request)
        return qs.annotate(favorites_count=Count("favorites_recipe"))


    def favorites_count(self, obj):
        return obj.favorites_count

    favorites_count.short_description = ("Favorites count")
    favorites_count.admin_order_field = "favorites_count"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "units",) 
    list_filter = ("name",)
    empty_value_display = "-пусто-"



admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe_composition)
admin.site.register(Tag)
admin.site.register(Recipe_tag)
admin.site.register(Follow)
admin.site.register(Favorites)
admin.site.register(Shop_list)
