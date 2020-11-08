from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=40, unique=True)

    def __str__(self):
       return self.title

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=20)

    def __str__(self):
       return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_post")
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    time = models.IntegerField("Cooking time")
    image = models.ImageField(upload_to='posts/')

    def __str__(self):
       return self.title


class Recipe_composition(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="recipe_ingredient")
    amount = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_composition")

    def __str__(self):
       return self.ingredient


class Recipe_tag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="tag_recipe")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="recipe_tag")


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey( User, on_delete=models.CASCADE, related_name="following")


class Favorites(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorites_recipe")
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name="favorites_recipe_user")

class Shop_list(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="shop_list_recipe")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shop_list_recipe_user")