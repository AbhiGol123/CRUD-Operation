from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'email', 'mobile_number', 'image', 'is_updated']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_updated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
