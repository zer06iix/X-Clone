from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import PostSerializer
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Posts

# Postss = [
#     {
#         "author":"Sarah",
#         "title":"spiderman",
#         "content":"Posts1-content",
#         "date_posted":"1996"
#     },
#     {
#         "author":"Ali",
#         "title":"batman",
#         "content":"Posts2-content",
#         "date_posted":"2006"
#     }
# ]


# def home(request):
#     context = {
#         'Postss': Postss.objects.all()
#     }
#     return render(request, "blog/home.html", context)

class PostListView(ListView):
    model = Posts
    # <app>/<model>_<viewtype>.html
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = 5

class UserPostListView(ListView):
    model = Posts
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Posts


class PostList(APIView):
    def get(self, request):
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self):
        pass


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        Posts = self.get_object()
        if self.request.user == Posts.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/'

    def test_func(self):
        Posts = self.get_object()
        if self.request.user == Posts.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", {'title': 'About'})
