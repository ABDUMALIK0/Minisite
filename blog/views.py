from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout, login
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import CommentForm, SigninForm
from .models import Post, Category, Tag, Comment
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('blog:index')

def signin_view(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password'],
                                        first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        email=request.POST['email'],
                                        )
        if user is not None:
            user.is_active = True
            #user.is_superuser = False
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('blog:index')
        else:
            return redirect('blog:index')
    else:
        form = SigninForm()
    return render(request, 'blog/signin.html', {'form':form})

def category_card_test(request, slug):
    if slug == 'no_category':
        category = 'None Category'
        post_list = Post.objects.filter(category=None)
    elif slug == 'none':
        category = 'Empty List'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    context = {
        'post_list':  post_list ,
        'categories':  Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'category': category,
    }
    return render(request, 'blog/index.html', context)

class PostList(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pk'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    login_url = 'blog:login'
    success_url = '/'
    fields = ['title', 'hook_text', 'content','head_image','file_upload', 'category', 'tags']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('blog:index')
        
class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    login_url = 'blog:login'
    template_name = 'blog/category_temp.html'
    template_name_field = 'form'
    fields = '__all__'
    success_url = 'blog:index'

class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    login_url = 'blog:login'
    template_name = 'blog/tag_temp.html'
    template_name_field = 'form'
    fields = '__all__'
    success_url = 'blog:index'
    
        
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    login_url = 'blog:login'
    template_name_field = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    login_url = 'blog:login'
    fields = ['title', 'hook_text', 'content','head_image','file_upload', 'category', 'tags']
    success_url = '/'
    template_name = 'blog/update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    login_url = 'blog:login'
    success_url = '/'
    template_name = 'blog/delete.html'

    def delete(self, request, *args, **kwargs):
        return super(PostDelete, self).delete(request, *args, **kwargs)

class CommentCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    login_url = 'blog:login'
 
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form):
        current_user = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.post = post
            form.instance.author = current_user
            return super(CommentCreate, self).form_valid(form)
        else:
            return PermissionDenied
   
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else: raise PermissionDenied

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    form_class = CommentForm
    template_name_suffix = '_form'
    

    def get_success_url(self, pk):
        post = Post.objects.get(pk=pk)
        return post.get_absolute_url()
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        success_url = self.get_success_url(kwargs['post'])
        return HttpResponseRedirect(success_url)
    
class PostSearch(PostList):
    paginate_by = None
    
    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q)| Q(tags__name__contains=q)
        ).distinct()
        return post_list
    
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context  