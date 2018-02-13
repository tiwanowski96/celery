from django import forms
from .models import Website, WebsiteCategory


class WebsiteCategoryAddForm(forms.ModelForm):
    class Meta:
        model = WebsiteCategory
        fields = [
            'name',
            'description'
        ]

class WebsiteAddForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = [
            'url',
            'category'
        ]
