from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def registration(request):
    EUMFO=UserMF()
    EPMFO=ProfileMF()
    d={'EUMFO':EUMFO,'EPMFO':EPMFO}
    if request.method=='POST' and request.FILES:
        NMUMFDO=UserMF(request.POST)
        NMPMFDO=ProfileMF(request.POST,request.FILES)
        if NMUMFDO.is_valid() and NMPMFDO.is_valid():
            MUMFDO=NMUMFDO.save(commit=False)
            pw=NMUMFDO.cleaned_data['password']
            MUMFDO.set_password(pw)
            MUMFDO.save()
            MPMFDO=NMPMFDO.save(commit=False)
            MPMFDO.username=MUMFDO
            MPMFDO.save()
            
            send_mail('registration successful', # subject,
                    'you have been registered successfully', # message,
                    'user@gmail.com', # from email,
                    [MUMFDO.email], # to email,
                    fail_silently=False )
            
            return HttpResponse('registration successful')
            
        else:
            return HttpResponse('Invalid Data')
    
    
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


def display_details(request):
    LUN=request.session.get('username')
    UO=User.objects.get(username=LUN)
    PO=Profile.objects.get(username=UO)
    
    d={'UO':UO,'PO':PO}
    
    
    return render(request,'display_details.html',d)


@login_required
def change_password(request):

    if request.method=='POST':
        pw=request.POST['password']

        un=request.session.get('username')
        UO=User.objects.get(username=un)

        UO.set_password(pw)
        UO.save()
        return HttpResponse('password is changed successfully')

    return render(request,'change_password.html')


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

