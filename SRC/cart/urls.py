from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.detail, name='detail'),
    path('add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:book_id>/', views.cart_remove, name='cart_remove'),
]