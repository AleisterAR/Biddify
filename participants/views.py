from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.user_type == 'admin':
                return redirect('/admin/')
            else:
                return redirect('')
    else:
        form = AuthenticationForm()
    
    return render(request, 'utilities/login.html', {'form': form})

def user_dashboard(request):
    return render(request, 'utilities/home.html')