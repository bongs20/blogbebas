from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Value, Q
from django.utils import timezone
from .models import Post, Comment, Vote, Category, PostAttachment, CommentAttachment
from .forms import RegisterForm, PostForm, CommentForm, CategoryForm, ProfileForm
from django.contrib.auth.models import User


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request, category_slug=None):
    sort = request.GET.get('sort', 'new')
    cat_query = request.GET.get('q')
    # Annotate score using SUM of vote values; when no votes, treat as 0
    posts_qs = Post.objects.select_related('author__profile', 'category').annotate(score=Sum('votes__value'))
    current_category = None
    if category_slug:
        current_category = Category.objects.filter(slug=category_slug).first()
        if current_category:
            posts_qs = posts_qs.filter(category=current_category)
    if sort == 'top':
        posts_qs = posts_qs.order_by('-score', '-created_at')
    else:
        posts_qs = posts_qs.order_by('-created_at')

    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all().order_by('name')
    if cat_query:
        categories = categories.filter(name__icontains=cat_query)
    categories = categories[:20]
    # Posts of the day: posts created today or with comments today, ranked by comments today then recency
    today = timezone.localdate()
    posts_of_the_day = (
        Post.objects.filter(Q(created_at__date=today) | Q(comments__created_at__date=today))
        .annotate(comments_today=Count('comments', filter=Q(comments__created_at__date=today), distinct=True))
        .order_by('-comments_today', '-created_at')
        .distinct()[:5]
    )
    return render(request, 'home.html', {
        'page_obj': page_obj,
        'sort': sort,
        'categories': categories,
        'current_category': current_category,
        'q': cat_query,
        'posts_of_the_day': posts_of_the_day,
    })


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()
            messages.success(request, 'Category created.')
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})


@login_required
def category_verify(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Not allowed')
        return redirect('home')
    cat = get_object_or_404(Category, slug=slug)
    cat.is_verified = True
    cat.save(update_fields=['is_verified'])
    messages.success(request, f'Verified r/{cat.slug}')
    return redirect('home')


@login_required
def category_unverify(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Not allowed')
        return redirect('home')
    cat = get_object_or_404(Category, slug=slug)
    cat.is_verified = False
    cat.save(update_fields=['is_verified'])
    messages.info(request, f'Unverified r/{cat.slug}')
    return redirect('home')


@login_required
def category_delete(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Not allowed')
        return redirect('home')
    cat = get_object_or_404(Category, slug=slug)
    cat.delete()
    messages.success(request, 'Category deleted')
    return redirect('home')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).select_related('author__profile').order_by('created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            # Save attachment if provided
            f = form.cleaned_data.get('attachment')
            url = form.cleaned_data.get('attachment_url')
            if f or url:
                CommentAttachment.objects.create(comment=comment, file=f, url=url, content_type=(f.content_type if f else 'url'))
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # Save attachment if provided
            f = form.cleaned_data.get('attachment')
            url = form.cleaned_data.get('attachment_url')
            if f or url:
                PostAttachment.objects.create(post=post, file=f, url=url, content_type=(f.content_type if f else 'url'))
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'Not allowed')
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            f = form.cleaned_data.get('attachment')
            url = form.cleaned_data.get('attachment_url')
            if f or url:
                PostAttachment.objects.create(post=post, file=f, url=url, content_type=(f.content_type if f else 'url'))
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'Not allowed')
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'post_confirm_delete.html', {'post': post})


@login_required
def vote(request, pk, action):
    post = get_object_or_404(Post, pk=pk)
    value = 1 if action == 'up' else -1
    vote, created = Vote.objects.get_or_create(post=post, user=request.user, defaults={'value': value})
    if not created:
        if vote.value == value:
            vote.delete()
        else:
            vote.value = value
            vote.save()
    return redirect('post_detail', pk=pk)


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user and not request.user.is_staff:
        messages.error(request, 'Not allowed')
        return redirect('post_detail', pk=comment.post.pk)
    if request.method == 'POST':
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post_detail', pk=post_pk)
    return render(request, 'comment_confirm_delete.html', {'comment': comment})


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user and not request.user.is_staff:
        messages.error(request, 'Not allowed')
        return redirect('post_detail', pk=comment.post.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comment_form.html', {'form': form, 'comment': comment})


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).annotate(score=Sum('votes__value')).order_by('-created_at')
    total_upvotes = Vote.objects.filter(post__author=profile_user, value=1).count()
    badge = None
    if total_upvotes >= 100:
        badge = ('Popular', 'success')
    elif total_upvotes >= 25:
        badge = ('Rising', 'info')
    elif total_upvotes >= 5:
        badge = ('Newbie', 'secondary')
    return render(request, 'user_profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'total_upvotes': total_upvotes,
        'badge': badge,
    })


@login_required
def profile_settings(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_settings.html', {'form': form})
