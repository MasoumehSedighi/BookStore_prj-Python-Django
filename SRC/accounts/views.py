from django.shortcuts import render
from accounts.forms import UserLoginForm


# Create your views here.
def user_login(request):
    form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
