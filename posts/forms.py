from django import forms
from posts.models import Post


class UserCreateNewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', "image")
