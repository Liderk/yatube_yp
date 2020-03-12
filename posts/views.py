from django.shortcuts import render, get_object_or_404

from .models import Post, Group
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import user_create_new_post


def index(request):
    # одна строка вместо тысячи слов на SQL
    latest = Post.objects.order_by('-pub_date')[:11]
    # собираем тексты постов в один, разделяя новой строкой
    return render(request, "index.html", {"posts": latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})


def new_post(request):
    if request.method == 'POST':
        form = user_create_new_post(request.POST)
        return render(request, 'new_post.html', {'form': form})
    form = user_create_new_post()
    return render(request, 'new_post.html', {'form': form})

