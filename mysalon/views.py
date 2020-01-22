from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView 
from .models import *
from .forms import *
from django.utils import timezone
from django.contrib import messages

from django.shortcuts import render, get_object_or_404

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
    paginated_by=10
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
    

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("mysalon:detail",slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("mysalon:detail",slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("mysalon:detail",slug=slug)
    

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect('mysalon:detail',slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('mysalon:detail',slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('mysalon:detail',slug=slug) 
    
    
 