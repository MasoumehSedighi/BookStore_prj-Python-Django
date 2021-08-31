from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('active/<uidb64>/<token>/', views.RegisterEmail.as_view(), name='active'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/update/', views.user_update, name='update'),
    path('profile/history/', views.history_order, name='history'),
    path('profile/address/', views.address_profile, name='address_profile'),
    path('profile/address/update/<int:pk>/', views.AddressUpdateView.as_view(), name='update_address'),
    path('profile/address/delete/<int:pk>/', views.AddressDeleteView.as_view(), name='address_delete'),
    path('reset/', views.ResetPassword.as_view(), name='reset'),
    path('reset/done/', views.DonePassword.as_view(), name='reset_done'),
    path('confirm/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='password_reset_confirm'),
    path('confirm/done/', views.Complete.as_view(), name='complete'),
    path('profile/addbook/', views.BookCreateView.as_view(), name='book_new'),
    path('profile/addcategory/', views.CategoryCreateView.as_view(), name='category_new'),
    path('profile/listbook/', views.BookListView.as_view(), name='staff_book_list'),
    path('profile/deletebook/<int:pk>', views.BookDeleteView.as_view(), name='book_delete'),
    path('profile/updateebook/<int:pk>', views.BookUpdateView.as_view(), name='staff_book_update'),
    path('profile/address/new', views.user_add_address, name='address_new'),

]
