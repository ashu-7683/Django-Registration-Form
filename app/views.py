from django.shortcuts import render,redirect

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from app.models import OTPModel
from django.contrib.auth.models import User
from django.utils import timezone


def registration(request):
    EUMFO=UserForm()
    EPMFO=ProfileForm()
    d={'EUMFO':EUMFO,'EPMFO':EPMFO}

    if request.method=='POST' and request.FILES:
        NMUFDO=UserForm(request.POST)
        NMPFDO=ProfileForm(request.POST,request.FILES)
        if NMUFDO.is_valid() and NMPFDO.is_valid():
            MUFDO=NMUFDO.save(commit=False)
            pw=NMUFDO.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()
            #Done with User model 

            MPFDO=NMPFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail('Registration',
                    'Ur registration is Successfull',
                    'ashutoshkhilar5@gmail.com',
                    [MUFDO.email],
                    fail_silently=False)
            return HttpResponse('registration is Successfull')
    

    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    
    return render(request,'home.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)

        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Credentials')

    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_display(request):
    loggedInUsername=request.session.get('username')
    UO=User.objects.get(username=loggedInUsername)
    PO=Profile.objects.get(username=UO)

    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        loggedInUsername=request.session.get('username')
        UO=User.objects.get(username=loggedInUsername)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('ur password is changed')
    return render(request,'change_password.html')

@login_required
def reset_password(request):

    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LUO=User.objects.filter(username=un)

        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('password reset is done')
        else:
            return HttpResponse('user is not present in my DB')
        

        return HttpResponse('Reset password is done successfully')
    return render(request,'reset_password.html')


# forget password functionality using OTP

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        
        if user:
            otp = OTPModel.generate_otp()
            OTPModel.objects.create(user=user, otp=otp)
            
            send_mail(
                'Password Reset OTP',
                f'Your OTP is: {otp}. Valid for 10 minutes.',
                'ashutoshkhilar5@gmail.com',
                [email],
                fail_silently=False
            )
            
            request.session['reset_user_id'] = user.id
            return redirect('verify_otp')
        
        return HttpResponse('Email not registered')
    
    return render(request, 'forget_password.html')

# Verify OTP
def verify_otp(request):
    if 'reset_user_id' not in request.session:
        return redirect('forget_password')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        user_id = request.session['reset_user_id']
        
        otp_obj = OTPModel.objects.filter(
            user_id=user_id, 
            is_used=False
        ).order_by('-created_at').first()
        
        if otp_obj and not otp_obj.is_expired() and otp_obj.otp == entered_otp:
            otp_obj.is_used = True
            otp_obj.save()
            request.session['otp_verified'] = True
            return redirect('set_new_password')
        
        return HttpResponse('Invalid or expired OTP')
    
    return render(request, 'verify_otp.html')

# Set New Password
def set_new_password(request):
    if not request.session.get('otp_verified'):
        return redirect('forget_password')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user_id = request.session['reset_user_id']
            user = User.objects.filter(id=user_id).first()
            
            if user:
                user.set_password(new_password)
                user.save()
                
                # Clear session
                request.session.pop('reset_user_id', None)
                request.session.pop('otp_verified', None)
                
                return HttpResponse('Password reset successful! You can now login.')
        
        return HttpResponse('Passwords do not match')
    
    return render(request, 'set_new_password.html')