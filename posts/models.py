from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=400)

    def __str__(self):
        # выводим название группы там где на это запрос пойдет
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True, db_index=True)
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE, related_name="group_posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        # выводим текст поста
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts_comment")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        # выводим текст коммента
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")


