from django import forms
from .models import Recipe
from .models import Recipe_composition
from .models import Tag


class NewRecipe(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form__input"})
        self.fields["text"].widget.attrs.update({"class": "form__textarea", "rows": "8"})
        self.fields["time"].widget.attrs.update({"class": "form__input", "min": "0"})
        self.fields["image"].widget.attrs.update({"class": "card__image", "id": "id_file"})


    class Meta():
        # Модель, с которой связана создаваемая форма
        model = Recipe
        # Поля, которые должны быть видны в форме и в каком порядке
        fields = ("title", "text", "time", "image")
        labels = {
            "title": "Название рецепта",
            "text": "Описание",
            "time": "Время приготовления",
            "image": "Загрузить фото",

        }


class NewRecipeComp(forms.Form):
    ingredient = forms.CharField(required=False)
    amount = forms.IntegerField(required=False)

    ingredient.widget.attrs.update({"class": "form__input", "id": "nameIngredient"})
    amount.widget.attrs.update({"class": "form__input", "id": "cantidad", "min": "0"})


class TagForm(forms.Form):
    breakfast = forms.BooleanField(label="Завтрак", required=False)
    lunch = forms.BooleanField(label="Обед", required=False)
    dinner = forms.BooleanField(label="Ужин", required=False)

    breakfast.widget.attrs.update({"id": "id_breakfast", "class": "tags__checkbox tags__checkbox_style_orange"})
    lunch.widget.attrs.update({"id": "id_lunch", "class": "tags__checkbox tags__checkbox_style_green"})
    dinner.widget.attrs.update({"id": "id_dinner", "class": "tags__checkbox tags__checkbox_style_purple"})

    def clean(self):
        breakfast = self.cleaned_data.get('breakfast')
        lunch = self.cleaned_data.get('lunch')
        dinner = self.cleaned_data.get('dinner')
        if not breakfast and not lunch and not dinner:
            raise forms.ValidationError("Выберите хотя бы один тег")
        return self.cleaned_data