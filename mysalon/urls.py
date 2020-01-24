from django.urls import path,include
from .views import (
    HomeView,
    ItemDetailView,
   
)
app_name = 'mysalon'
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('home/',HomeView.as_view(),name='home'),
    path('product/<slug>/',ItemDetailView.as_view(),name="detail"),
    path('',views.posts,name="posts"),
    path('what_we_do/' ,views.what_we_do,name='what-we-do'),
    path('comment/<int:id>',views.add_comments,name='comment'),
    path('add-to-cart/<slug>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>',views.remove_from_cart,name='remove_from_cart'),
    path('order_summary/',views.order_summary,name='order-summary'),
    path('remove_item/<slug>',views.remove_single_item_from_cart,name='remove_one'),
    path('create_appointment/',views.create_appointment,name="appointment"),
    path('paypal_return/',views.paypal_return,name="return"),
    #Dashboard
    path('activate/user/<int:user_id>', views.user_activate, name='activate_user'),
    path('deactivate/user/<int:user_id>', views.user_deactivate, name='deactivate_user'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('users/', views.registered_users, name='system_users'),
    
    #paypal
    path('go/',include,('paypal.standard.ipn.urls')),
    path('pay_total/',views.total_order,name='make_payment'),
]

