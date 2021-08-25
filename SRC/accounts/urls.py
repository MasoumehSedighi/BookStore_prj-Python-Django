from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/update', views.user_update, name='update'),
    path('profile/history', views.history, name='history'),
    path('reset/', views.ResetPassword.as_view(), name='reset'),
    path('reset/down/', views.DonePassword.as_view(), name='reset_done'),
    path('confirm/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='password_reset_confirm'),
    path('confirm/done/', views.Complete.as_view(), name='complete')
]
