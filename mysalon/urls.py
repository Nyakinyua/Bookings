from django.urls import path
from .views import (
    HomeView,
    ItemDetailView,
)

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('product/<slug>/',ItemDetailView.as_view(),name="detail"),
    path('post/',views.posts,name="posts"),
    path('comment/<int:id>',views.add_comments,name='comment'),
    
]