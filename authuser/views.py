from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from hr.models import Hr

def register_candidate(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            msg = "password didn't match"
            return render(request, 'authuser/candidateregister.html', {'msg':msg})
        if User.objects.filter(username=username).exists():
            msg = "Username already Exists"    
            return render(request, 'authuser/candidateregister.html', {'msg':msg}) 
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request,user)
        return redirect('candidate_dashboard')
    return render(request, 'authuser/candidateregister.html')

def register_hr(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
      
        if password != cpassword:
            msg = "password didn't match"
            return render(request, 'authuser/candidateregister.html', {'msg':msg})
        if User.objects.filter(username=username).exists():
            msg = "Username already exists"    
            return render(request, 'authuser/candidateregister.html', {'msg':msg}) 
        user = User.objects.create_user(username=username, email=email, password=password)
        Hr(user=user).save()
        login(request,user)
        return redirect('hr_dash')
 
    return render(request, 'authuser/hrregister.html')

def login_user(request):
    msg = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username=username, password=password)
        if user is not None:
            login(request, user)  
            if Hr.objects.filter(user=user).exists():
                return redirect('hr_dash')
            else:
                return redirect('candidate_dashboard')
        else:
            msg = "Username and Password didn't match"    
    
    return render(request, 'authuser/login.html' , {'msg':msg})

def logout_user(request):
    logout(request)
    return redirect('login_user')
