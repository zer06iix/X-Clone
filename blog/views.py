from django.shortcuts import render
from django.http import HttpResponse
from .models import Posts
from django.contrib.auth.models import User

# posts = [
#     {
#         "author":"Sarah",
#         "title":"spiderman",
#         "content":"post1-content",
#         "date_posted":"1996"
#     },
#     {
#         "author":"Ali",
#         "title":"batman",
#         "content":"post2-content",
#         "date_posted":"2006"
#     }
# ]


def home(request):
    context = {
        'posts': Posts.objects.all()
    }
    return render(request, "blog/home.html", context)


def about(request):
    return render(request, "blog/about.html", {'title': 'About'})
