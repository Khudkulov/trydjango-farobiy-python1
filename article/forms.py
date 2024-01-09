from django import forms
from .models import Article
from django.forms import ValidationError


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'placeholder': 'title... form'
        })
        self.fields['content'].widget.attrs.update({
             'cols': 60,
             'rows': 5,
             'placeholder': 'content... form',

        })

    def clean_title(self):   # clean_'name
        if self.cleaned_data['title'].replace(' ', '').isalnum():
            return self.cleaned_data['title']
        raise ValidationError('Title must be alpha numeric')
