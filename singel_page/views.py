from django.shortcuts import render
from blog.models import Post
# Create your views here.
def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(request, 'singel_page/landing.html',{'recent_posts':recent_posts})
def about_me(request):
    return render(request, 'singel_page/about_me.html')