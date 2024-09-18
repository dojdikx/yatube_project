from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Group
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .utils import get_page_context
from .forms import PostForm

User = get_user_model()
# Главная страница
@login_required
def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)

# Страница с груп постами;
# view-функция принимает параметр pk из path()
@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]

    context = {
        'group': group,
        'posts': posts,
    }
    return render(request,'posts/group_list.html', context)
@login_required
def profile(request, username):
    author = get_object_or_404(User, username=username)
    page_obj = Post.objects.filter(author=author).order_by('-pub_date')


    context = {
        'page_obj': get_page_context(request, page_obj),
        'author': author,
    }
    return render(request, 'posts/profile.html', context)
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author

    context = {
        'post': post,
        'author': author,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    groups = Group.objects.all()
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user.username)

    context = {
        'form': form,
        'groups': groups,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)

    groups = Group.objects.all()  # Получаем все группы для выбора

    context = {
        'form': form,
        'is_edit': True,  # Указывает на режим редактирования
        'post': post,
        'groups': groups,  # Передаем группы в контекст
    }
    return render(request, 'posts/create_post.html', context)
