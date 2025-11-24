from django.shortcuts import render

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
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate OTP
                otp = OTPModel.generate_otp()
                # Save OTP to database
                OTPModel.objects.create(user=user, otp=otp)
                
                # Send OTP via email
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is: {otp}. This OTP is valid for 10 minutes.',
                    'ashutoshkhilar5@gmail.com',
                    [email],
                    fail_silently=False,
                )
                
                # Store user ID in session for verification
                request.session['reset_user_id'] = user.id
                request.session['reset_email'] = email
                
                return HttpResponseRedirect(reverse('verify_otp'))
                
            except User.DoesNotExist:
                return HttpResponse("No user found with this email address.")
    else:
        form = EmailForm()
    
    return render(request, 'forget_password.html', {'form': form})

def verify_otp(request):
    # Check if user came from forget password
    if 'reset_user_id' not in request.session:
        return HttpResponseRedirect(reverse('forget_password'))
    
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            user_id = request.session['reset_user_id']
            
            try:
                # Get the latest OTP for this user that's not used and not expired
                otp_obj = OTPModel.objects.filter(
                    user_id=user_id, 
                    is_used=False
                ).latest('created_at')
                
                if otp_obj.is_expired():
                    return HttpResponse("OTP has expired. Please request a new one.")
                
                if otp_obj.otp == otp_entered:
                    # Mark OTP as used
                    otp_obj.is_used = True
                    otp_obj.save()
                    
                    # Store verification in session
                    request.session['otp_verified'] = True
                    return HttpResponseRedirect(reverse('set_new_password'))
                else:
                    return HttpResponse("Invalid OTP. Please try again.")
                    
            except OTPModel.DoesNotExist:
                return HttpResponse("OTP not found or already used. Please request a new one.")
    else:
        form = OTPForm()
    
    return render(request, 'verify_otp.html', {'form': form})

def set_new_password(request):
    # Check if OTP is verified
    if 'reset_user_id' not in request.session or not request.session.get('otp_verified'):
        return HttpResponseRedirect(reverse('forget_password'))
    
    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            user_id = request.session['reset_user_id']
            new_password = form.cleaned_data['new_password']
            
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                
                # Clear session data
                request.session.pop('reset_user_id', None)
                request.session.pop('reset_email', None)
                request.session.pop('otp_verified', None)
                
                # Send confirmation email
                send_mail(
                    'Password Reset Successful',
                    'Your password has been reset successfully.',
                    'ashutoshkhilar5@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                
                return HttpResponse("Password reset successfully! You can now login with your new password.")
                
            except User.DoesNotExist:
                return HttpResponse("User not found.")
    else:
        form = NewPasswordForm()
    
    return render(request, 'set_new_password.html', {'form': form})