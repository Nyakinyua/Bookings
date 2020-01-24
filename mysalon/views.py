from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from .models import *
from .forms import *
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import random


# Create your views here.
@login_required()
def item_list(request):
    context = {
        'item': Item.objects.all()
    }
    return render(request, 'homepage.html', context)

@login_required()
def item_list(request):
    context = {
        'item': Item.objects.all()
    }
    return render(request, 'homepage.html', context)

@login_required()
def order_summary(request):
    try:
        order = Order.objects.get(user=request.user,ordered=False)
        return render(request,'order_summary.html',{'object':order})
    except ObjectDoesNotExist:
        messages.warning(self.request,"You do not have an active order")
@login_required()       
def total_order(request):
    if request.method == 'POST':
        amount = request.POST.get('price')
        paypal_dict = {
            "business":settings.PAYPAL_RECEIVER_EMAIL,
            "amount":amount,
            "item_name":'Products',
            "invoice":str(random.randint(000,999)),
            "currency_code":'USD',
            "notify_url":'',
            "return_url":'',
            "cancel_return":'',
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request,'payment.html',{"form":form})


class HomeView(ListView):
    model = Item
    paginated_by = 10
    template_name = 'homepage.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'

@login_required()
def posts(request):
    
    return render(request, 'index.html')

def what_we_do(request):
    all_posts = Salonposts.objects.all()
    comments = Comments.objects.all()
    return render(request, 'posts.html', {'post': all_posts, 'comments': comments})


@login_required()
def add_comments(request, id):
    '''
    view function that renders one post and has a comment section
    '''
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            post = Salonposts.objects.get(id=id)
            comment.post = post
            comment.save()
            return redirect('comment', id=id)
    else:
        form = AddCommentForm()
        post = Salonposts.get_one_post(id)
        posts = Salonposts.objects.get(id=id)
        comment = Comments.objects.filter(post=post.id)
        return render(request, 'comment.html', {'form': form, 'post': post, 'comments': comment})

@login_required()
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
            return redirect('mysalon:order-summary')
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("mysalon:detail", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("mysalon:detail", slug=slug)

@login_required()
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
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect('mysalon:order-summary')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('mysalon:detail', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('mysalon:detail', slug=slug)

@login_required()
def remove_single_item_from_cart(request, slug):
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
            return redirect('mysalon:order-summary')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('mysalon:detail', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('mysalon:detail', slug=slug)

@login_required()
def user_dashboard(request):
    """
    function for displaying dashboard
    """
    return render(request, 'dashboard.html')

@login_required()
def registered_users(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'users.html', context)

@login_required()
def user_deactivate(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    messages.success(request, "User account has been successfully deactivated!")
    return redirect('system_users')

@login_required()
def user_activate(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    messages.success(request, "User account has been successfully activated!")
    return redirect('system_users')

def create_appointment(request):
    user = request.user
    if request.method == 'POST':
        booked = Appointment.objects.all()
        for book in booked:
            if Appointment.user == request.user:
                messages.info(request,"You have a pending appointment")
                return redirect('mysalon:home')
        email = request.POST.get('email')
        number = request.POST.get('phone')
        date = request.POST.get('appointment')
        service = request.POST.get('service')
        
        
        if email and number and date and service:
            your_appointment = Appointment(user = request.user,email=email,contact=number,date=date,service=service)
            your_appointment.save()
            messages.info(request,"Your appointment has been scheduled on")
            return redirect('mysalon:home')
        else:
            messages.info(request,"Input all fields")
            return redirect('mysalon:appointment')
    else:
        messages.info(request,'Invalid Inputs, try again')
        return render(request,"appointments.html")
         
           
                
            
        
        