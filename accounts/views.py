from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .send_code import generate_confirm_code, email_yuborish


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect("/")
        else:
            messages.error(request, 'Logged in Fail')
            return redirect('login')
        
    return render(request, "accounts/login.html")


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get("email")
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
    
        if not username or not password1 or not password2:
            messages.error(request, 'All fields are required.')
            return redirect('signup')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        
        if len(password1) < 8:
            messages.error(request, "Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username mavjud.')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email band.')
            return redirect('signup')
        
        confirm_code = generate_confirm_code()
        email_yuborish(email, "Tasdiqlash kodi", f"Tasdiqlash kodingiz: {confirm_code}")
        
        request.session['signup_data'] = {
            'username': username,
            'email': email,
            'password1': password1,
            'confirm_code': confirm_code
        }
            
        return redirect('confirm') 
    return render(request, 'accounts/signup.html')


def confirm(request):
    signup_data = request.session.get("signup_data")
    
    if request.method == 'POST':
        code = int(f"{request.POST['code1']}{request.POST['code2']}{request.POST['code3']}{request.POST['code4']}")
        if int(signup_data['confirm_code']) == code:
            user = User.objects.create_user(
                username=signup_data["username"],
                email=signup_data["email"],
                password=signup_data["password1"]
            )
            user.save()
            del request.session['signup_data']
            messages.success(request, 'Hisob muvoffaqiyatli yaratildi!')
            return redirect('login')
        else:
            messages.error(request, 'Kod xato. Qayta kiriting')

    return render(request, "accounts/confirm.html", {"email": signup_data['email']})
    
    
def logout_view(request):
    logout(request)
    return redirect("/")