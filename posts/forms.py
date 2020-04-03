from django import forms
from posts.models import Post, Comment


class UserCreateNewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', "image")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )