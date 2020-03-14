from django import forms
from posts.models import Post


class User_Create_New_Post(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text',)
