from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='create'),
    path('<int:order_id>/', views.detail, name='detail'),
    path('apply/<int:order_id>/', views.coupon_apply, name='coupon_apply'),
    path('complete_order/<int:order_id>/', views.complete_order, name='complete_order'),
    path('address_add/<int:order_id>/', views.add_address, name='add_address'),


]