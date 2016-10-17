#coding=utf-8
from django import forms
from django.core.exceptions import ValidationError

from app.models import UserProfile

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

class UserProfileForm(forms.ModelForm):
    error_css_class = 'error'
    class Meta:
        model = UserProfile
        fields = [
            'profile_image', 'sex'
        ]

        labels = {
            'profile_image': '头像',
            'sex':'性别',
        }

        widgets = {
            'profile_image': forms.FileInput(
                attrs={'class': 'ui input'},
            )
        }


class PasswordForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"原密码",
            }
        ),
    )
    newpassword1 = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"新密码",
            }
        ),
    )
    newpassword2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"确认密码",
            }
        ),
     )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(PasswordForm, self).clean()
        return cleaned_data