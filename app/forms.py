#coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
import re

def words_vaildator(name):
    if len(name) < 4:
        raise ValidationError('太短了!')

def word_filter(comment):
    words = ('fuck', 'dick', 'ass')
    for word in words:
        if re.search(word, comment):
            raise ValidationError('含有非法词语!')
        else:
            continue

class CommentForm(forms.Form):
    name = forms.CharField(max_length=50, validators=[words_vaildator])
    comment = forms.CharField(
        widget=forms.Textarea(
            # 可以修改,但不建议这么做
            # attrs={'class': 'item'},
        ),
        error_messages= {
            'required': '又不填!',
        },
        validators=[word_filter],
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Username',
            }
        )
    )
    password = forms.CharField()