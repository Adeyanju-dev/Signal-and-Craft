from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post

def home(request):
    posts = list(Post.objects.select_related("author").all())
    featured_post = next((post for post in posts if post.featured), posts[0] if posts else None)
    article_posts = [post for post in posts if not featured_post or post.pk != featured_post.pk]
    category_breakdown = (
        Post.objects.values("category")
        .annotate(total=Count("id"))
        .order_by("-total", "category")
    )
    return render(
        request,
        "posts/home.html",
        {
            "featured_post": featured_post,
            "article_posts": article_posts,
            "post_count": len(posts),
            "category_breakdown": category_breakdown,
        },
    )

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated and not post.author:
                post.author = request.user
            post.save()
            return redirect(post)
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {"form": form, "is_edit": False})

def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("author"), slug=slug)
    return render(request, "posts/post_detail.html", {"post": post})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated and not post.author:
                post.author = request.user
            post.save()
            return redirect(post)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "posts/post_form.html",
        {"form": form, "post": post, "is_edit": True},
    )

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, "posts/post_confirm_delete.html", {"post": post})

