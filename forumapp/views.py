from django.http import HttpResponse
from django.shortcuts import render, redirect
from forumapp.forms import PostDeleteForm, PostCreateForm, SearchForm, PostEditForm
from forumapp.models import Post


# Create your views here.
def dashboard(request):

    posts = Post.objects.all()
    form = SearchForm(request.GET or None)

    if request.method == 'GET':
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = posts.filter(title__icontains=query)

        context = {
            'posts': posts,
            'search_form': form
        }

        return render(request, 'posts/dashboard.html', context)


def index(request):
    return render(request, 'common/index.html')


def create_post(request):
     form = PostCreateForm(request.POST or None)

     if form.is_valid():
        form.save()
        return redirect('dashboard')

     context = {
         'post_create_form': form
     }

     return render(request, 'posts/create-post-page.html', context)


def delete_post_with_pk(request, pk):
    post = Post.objects.get(pk=pk)
    form = PostDeleteForm(instance=post)

    if request.method == 'POST':
        post.delete()
        return redirect('dashboard')

    context = {
        'delete_post_form': form,
        'post': post
    }

    return render(request, 'posts/delete-post.html', context)


def post_details(request, pk):
    post = Post.objects.get(pk=pk)

    context = {
        'post': post
    }

    return render(request, 'posts/post-details.html', context)

def search_post(request):
    return HttpResponse(f'Search post')


def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    form = PostEditForm(instance=post)

    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')

        else:
            PostEditForm(instance=post)

    context = {
            'post': post,
            'edit_post_form': form
        }

    return render(request, 'posts/edit-post.html', context)