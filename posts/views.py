from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required

from .models import Post, User, Group, Comment, Follow
from django.shortcuts import redirect
from .forms import UserCreateNewPost, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 3)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = get_list_or_404(Post.objects.order_by("-pub_date").all(), group=group)
    paginator = Paginator(posts, 10)
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


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author).order_by("-pub_date").all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = Follow.objects.filter(author=author, user=request.user.id)
    return render(request, "profile.html",
                  {'author': author, 'page': page, 'paginator': paginator, 'following': following, 'user': request.user.id})


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=author)
    if request.user != author:
        return redirect("post", username=request.user.username, post_id=post_id)
    form = UserCreateNewPost(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            post.save()
            return redirect("post", username, post_id)
        return render(request, 'new_post.html', {'form': form})
    form = UserCreateNewPost(instance=post)
    return render(request, 'new_post.html', {'form': form, 'post': post})


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=author)
    comments = Comment.objects.filter(post_id=post, ).all()
    posts_count = Post.objects.filter(author=author)
    form = CommentForm()
    return render(request, 'post.html',
                  {'form': form, 'post': post, 'comments': comments, 'posts_count': posts_count, 'author': author})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect("post", username, post_id)


@login_required
def follow_index(request):
    follower = Follow.objects.filter(user=request.user)
    authors = (item.author.id for item in follower)
    post_list = Post.objects.filter(author__in=authors).order_by('-pub_date').all()
    paginator = Paginator(post_list, 5)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'follow.html', {'page': page, 'paginator': paginator, 'follower': follower})


@login_required
def profile_follow(request, username):
    follower = User.objects.get(username=request.user)
    following = User.objects.get(username=username)
    if following == follower:
        return redirect('index')
    try:
        following = Follow.objects.get(user=follower, author=following)
    except Follow.DoesNotExist:
        Follow.objects.create(user=follower, author=following)
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    follower = User.objects.get(username=request.user)
    following = User.objects.get(username=username)
    unfollow_id = Follow.objects.filter(user=follower, author=following)
    unfollow_id.delete()
    return redirect('profile', username)
