from .models import Sale
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('count',)