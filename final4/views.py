from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from .models import Product, Sale
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
# Create your views here.

def index(request):
    return render(request, 'final4/index.html')

def buyProduct(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Product, pk=pk)

        if request.method=='POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.name = post
                comment.user = request.user
                comment.save()
                return redirect('/final4/product_list.html')
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

class ProductList(ListView):
    model = Product
    template_name = 'final4/product_list.html'
    context_object_name = 'product_list'
    paginate_by = 3

class ProductDetail(DetailView):
    model = Product
    template_name = 'final4/product_detail.html'
    #context_object_name = 'product_detail'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['comment_form'] = CommentForm
        
        return context
class CartList(ListView):
    model = Sale
    template_name = 'final4/sale_list.html'
