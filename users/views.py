from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def create_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}')
            return redirect('food:index')
    else:
        form = RegisterForm()
        
    return render(request, 'users/register.html', {'form':form})


# def logout_view(request):
#     logout(request)
#     # Redirige a la página de inicio o a donde desees que el usuario vaya después del logout.
#     return redirect('food:index')

@login_required
def profile_page(request):
    return render(request, 'users/profile.html')