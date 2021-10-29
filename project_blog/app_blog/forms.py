from django import forms
from django.db.models import fields
from django.forms.widgets import Textarea
from app_blog.models import comment


class share_blog(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=Textarea)

class comments_blog(forms.ModelForm):
    class Meta:
        model=comment
        fields=('name','email','body')

