from django_filters import (
    FilterSet, ModelChoiceFilter, CharFilter, DateTimeFilter,
)
from django import forms
from .models import *


class PosterFilter(FilterSet):
    user = ModelChoiceFilter(label='Author', empty_label='Any', queryset=User.objects.all())
    title = CharFilter(label='Title contains', lookup_expr='icontains')
    created = DateTimeFilter(
        label='Published after',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gt',
    )
    category = ModelChoiceFilter(label='Category', empty_label='Any', queryset=Category.objects.all())

    class Meta:
        model = Poster
        fields = [
            'title',
            'user',
            'created',
            'category',
        ]