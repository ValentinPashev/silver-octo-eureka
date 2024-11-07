from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from forumapp.forms import PostDeleteForm, PostCreateForm, SearchForm, CommentFormSet
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


class CreatePostView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/create-post-page.html'
    success_url = reverse_lazy('dashboard')


# def create_post(request):
#      form = PostCreateForm(request.POST or None)
#
#      if form.is_valid():
#         form.save()
#         return redirect('dashboard')
#
#      context = {
#          'post_create_form': form
#      }
#
#      return render(request, 'posts/create-post-page.html', context)


class PostDeleteView(DeleteView):
    model = Post
    form_class = PostDeleteForm
    success_url = reverse_lazy('dashboard')
    template_name = 'posts/delete-post.html'

    def get_initial(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        post = Post.objects.get(pk=pk)
        return post.__dict__


# def delete_post_with_pk(request, pk):
#     post = Post.objects.get(pk=pk)
#     form = PostDeleteForm(instance=post)
#
#     if request.method == 'POST':
#         post.delete()
#         return redirect('dashboard')
#
#     context = {
#         'delete_post_form': form,
#         'post': post
#     }
#
#     return render(request, 'posts/delete-post.html', context)


def post_details(request, pk):
    post = Post.objects.get(pk=pk)
    formset = CommentFormSet(request.POST or None)


    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    comment = form.save(commit=False)
                    comment.post = post
                    comment.save()
            return redirect('post_details', pk=post.id)

    context = {
        'post': post,
        'formset': formset,
    }

    return render(request, 'posts/post-details.html', context)

def search_post(request):
    return HttpResponse(f'Search post')



class EditPostView(UpdateView):
    model = Post
    template_name = 'posts/edit-post.html'
    success_url = reverse_lazy('dashboard')


    def get_form_class(self):
        if self.request.user.is_superuser:
            return modelform_factory(Post, fields='__all__')

        else:
            return modelform_factory(Post, fields='text',)

# def edit_post(request, pk):
#     post = Post.objects.get(pk=pk)
#     form = PostEditForm(instance=post)
#
#     if request.method == 'POST':
#         form = PostEditForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#         else:
#             PostEditForm(instance=post)
#
#     context = {
#             'post': post,
#             'edit_post_form': form
#         }
#
#     return render(request, 'posts/edit-post.html', context)