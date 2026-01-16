from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            username=request.POST['password']
        )
        
        if user:
            login(request, user)
            return redirect('dashboard')
        
    return render(request, 'accounts/login.html')