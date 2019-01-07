from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView, DetailView,CreateView,UpdateView,DeleteView)



# Create your views here.
# posts = [{
#         'author' : 'Yeashin',
#         'title' : 'Bolg 1',
#         'content' : 'My first blog',
#         'date_posted' : 'Jan 1, 2019'
#     },
#     {
#         'author' : 'Evan',
#         'title' : 'Blog 2',
#         'content' : 'My second blog',
#         'date_posted' : 'Jan 1, 2019'
#     }
# ]

def home_blog(request):
    context = { 'posts': Post.objects.all()}
    return render(request,'my_blog/home.html', context)

def about (request):
    return render(request,'my_blog/about.html', {'title': 'About'})

class PostListView(ListView):
    model = Post
    template_name= 'my_blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False