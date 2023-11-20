from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    ordering = 'date_posted'


class PostDetailView(DetailView):
    model = Posts


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
