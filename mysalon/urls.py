from django.urls import path
from .views import (
    HomeView,
    ItemDetailView,
)
app_name = 'mysalon'
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('product/<slug>/',ItemDetailView.as_view(),name="detail"),
    path('post/',views.posts,name="posts"),
    path('comment/<int:id>',views.add_comments,name='comment'),
    path('add-to-cart/<slug>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>',views.remove_from_cart,name='remove_from_cart'),
    
]

