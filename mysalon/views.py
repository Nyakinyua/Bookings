from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView 
from .models import *
from .forms import *

# Create your views here.
def item_list(request):
    context = {
        'item': Item.objects.all()
    }
    return render(request,'homepage.html',context)

def item_list(request):
    context = {
        'item': Item.objects.all()
    }
    return render(request,'homepage.html',context)

class HomeView(ListView):
    model = Item
    template_name = 'homepage.html'
    
class ItemDetailView(DetailView):
    model = Item
    template_name= 'product.html'

def posts(request):
    all_posts=Salonposts.objects.all()
    comments=Comments.objects.all()
    return render(request,'posts.html',{'post':all_posts,'comments':comments})

def add_comments(request,id):
    '''
    view function that renders one post and has a comment section
    '''
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user=request.user
            post=Salonposts.objects.get(id=id)
            comment.post=post
            comment.save()
            return redirect('comment',id=id)
    else:
        form = AddCommentForm()
        post = Salonposts.get_one_post(id)
        posts= Salonposts.objects.get(id = id)
        comment = Comments.objects.filter(post = post.id)
        return render(request,'comment.html',{'form':form,'post':post,'comments':comment})
    
def add_to_cart(request,slug):
    item = get_object_or_404(item,slug=slug)
    order_item = OrderItem.objects.create(item=item)