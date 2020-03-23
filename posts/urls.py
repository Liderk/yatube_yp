from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_post, name="new_post"),
    path("group/<slug:slug>/", views.group_posts, name="group_posts"),
    # Профайл пользователя
    path("user/<username>/", views.profile, name="profile"),
    # Просмотр записи
    path("user/<username>/<int:post_id>/", views.post_view, name="post"),
    path("user/<username>/<int:post_id>/edit", views.post_edit, name="post_edit"),

]