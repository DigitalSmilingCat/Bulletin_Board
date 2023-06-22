from django import forms
from .models import Poster, Response
from django.core.exceptions import ValidationError


class PosterForm(forms.ModelForm):
    class Meta:
        model = Poster
        fields = [
            'title',
            'content',
            'category',
        ]
        labels = {
            'title': 'Title',
            'content': '',
            'category': 'Category',
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is None:
            raise ValidationError({
                'title': 'Title cannot be empty'
            })
        return cleaned_data


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'text',
        ]
        labels = {
            'text': ''
        }