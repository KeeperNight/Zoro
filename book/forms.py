from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book,Chapter


class ChapterCreateForm(forms.ModelForm):
    books = forms.ModelChoiceField(queryset=Book.objects.none())
    
    class Meta:
        model = Chapter
        fields = ['name','content']

    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(ChapterCreateForm, self).__init__(*args, **kwargs)
        self.fields['books'].queryset=Book.objects.filter(author=author)