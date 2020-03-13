from django import forms
from posts.models import Post


class User_Create_New_Post(forms.ModelForm):
    # def clean_artist(self):
    #     post_text = self.cleaned_data['text']
    #     if post_text:
    #         return post_text
    #     raise forms.ValidationError("Вы должны что нибудь ввести")

    class Meta:
        model = Post
        fields = ('group', 'text',)
