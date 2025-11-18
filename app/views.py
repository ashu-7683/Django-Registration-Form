from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse

def registration(request):
    EUMFO=UserMF()
    EPMFO=ProfileMF()
    d={'EUMFO':EUMFO,'EPMFO':EPMFO}
    if request.method=='POST':
        UMFDO=UserMF(request.POST)
        PMFDO=ProfileMF(request.POST,request.FILES)
        if UMFDO.is_valid() and PMFDO.is_valid():
            NSU=UMFDO.save()
            password=UMFDO.cleaned_data['password']
            NSU.set_password(password)
            NSU.save()
            NPS=PMFDO.save()
            NPS.username=NSU
            NPS.save()
            #show the registered data
            return HttpResponse(str(EUMFO.cleaned_data))
            
        else:
            return HttpResponse('Invalid Data')
    
    
    return render(request,'registration.html',d)