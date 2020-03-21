from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Post, User, Group
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import UserCreateNewPost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, 'page': page, 'paginator': paginator})

@login_required
# исползуем декоратор, если пользователь не авторизован, то перенаправляем его login.html по адресу прописанном
# в settings.LOGIN_URL. Если авторизован, то выполняется код представления
def new_post(request):
    if request.method == 'POST':
        form = UserCreateNewPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'new_post.html', {'form': form})
    form = UserCreateNewPost()
    return render(request, 'new_post.html', {'form': form})
