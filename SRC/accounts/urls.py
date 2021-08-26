from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/update/', views.user_update, name='update'),
    path('profile/history/', views.history_order, name='history'),
    path('profile/address/', views.address_profile, name='address_profile'),
    path('profile/address/update/<int:address_id>/', views.update_address, name='update_address'),
    path('reset/', views.ResetPassword.as_view(), name='reset'),
    path('reset/down/', views.DonePassword.as_view(), name='reset_done'),
    path('confirm/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='password_reset_confirm'),
    path('confirm/done/', views.Complete.as_view(), name='complete'),
    path('profile/addbook/', views.BookCreateView.as_view(), name='book_new'),
    path('profile/addcategory/', views.CategoryCreateView.as_view(), name='category_new'),
]
