from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('created_at')
    return render(request, 'posts/home.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            Post.objects.create(title=title, content=content)
            return redirect('home')
    return render(request, 'posts/post_form.html', {'form_type' :'template'})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        return redirect('post-detail', pk=pk)
    
    return render(request, 'posts/post_form.html', {'post': post, 'form_type': 'Edit' })

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

