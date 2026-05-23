"""Projects - Forms"""
from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'home_type', 'area', 'rooms', 'bathrooms', 'floors',
                  'repair_type', 'address', 'description', 'budget', 'has_smart_home', 'floor_plan']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Loyiha nomi'}),
            'area': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'kv.m', 'step': '0.5'}),
            'rooms': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 20}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 10}),
            'floors': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 50}),
            'budget': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': "So'm"}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Manzil'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'home_type': forms.Select(attrs={'class': 'form-select'}),
            'repair_type': forms.Select(attrs={'class': 'form-select'}),
            'has_smart_home': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'floor_plan': forms.FileInput(attrs={'class': 'form-file', 'accept': 'image/*'}),
        }
