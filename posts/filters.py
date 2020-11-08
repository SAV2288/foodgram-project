from django.db import models
import django_filters
from django import forms


class TagFilter(django_filters.FilterSet):
    breakfast = django_filters.BooleanFilter(label="Завтрак", widget=forms.CheckboxInput, method="filter_tags")
    lunch = django_filters.BooleanFilter(label="Обед", widget=forms.CheckboxInput, method="filter_tags")
    dinner = django_filters.BooleanFilter(label="Ужин", widget=forms.CheckboxInput, method="filter_tags")


    def filter_tags(self, queryset, name, value):

        data = ["breakfast", "lunch", "dinner"]

        params = {}
        for item in data:
            params[item] = self.form.data.get(item, "")

        fields_on = [ item for item, value in params.items() if value == "on" ]

        if value:
            queryset = queryset.filter( tag_recipe__tag__title__in=fields_on )
        return queryset

