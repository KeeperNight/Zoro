from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book,Chapter

class ChapterCreateForm(forms.ModelForm):
    book = forms.ModelChoiceField(queryset=Book.objects.none())
    
    class Meta:
        model = Chapter
        fields = ['name','content','author','book']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ChapterCreateForm, self).__init__(*args, **kwargs)
        self.fields['book'].queryset=Book.objects.filter(author=user)