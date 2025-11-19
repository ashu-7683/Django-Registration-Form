from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse

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
            
            return HttpResponse('registration successful')
            
        else:
            return HttpResponse('Invalid Data')
    
    
    return render(request,'registration.html',d)