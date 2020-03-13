from django import forms
from django.db import models
from posts.models import Post, User


class user_create_new_post(forms.ModelForm):
    def clean_artist(self):
        post_text = self.cleaned_data['text']
        if post_text:
            return post_text
        raise forms.ValidationError("Вы должны что нибудь ввести")

    class Meta:
        model = Post
        fields = ('group', 'text',)
