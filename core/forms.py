# core/forms.py
from django import forms
from .models import UserWord

class WordCreateForm(forms.ModelForm):
    class Meta:
        model = UserWord
        fields = ["word", "meaning",]
        widgets = {
            "word": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "単語を入力"
            }),
            "meaning": forms.Textarea(attrs={
                "class": "textarea",
                "placeholder": "意味を自由に入力してください",
                "rows": 5,
            }),
        }
