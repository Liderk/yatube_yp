from django import forms


from posts.models import Post


class user_create_new_post(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text',)
