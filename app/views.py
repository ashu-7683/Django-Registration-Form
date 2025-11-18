from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse

def registration(request):
    EUMFO=UserMF()
    EPMFO=ProfileMF()
    d={'EUMFO':EUMFO,'EPMFO':EPMFO}
    
    return render(request,'registration.html',d)