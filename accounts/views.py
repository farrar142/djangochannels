from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import User
from .forms import UserForm

# Create your views here.
#

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        messages.success(request,form)
        if form.is_valid():
            signed_user = form.save()
            messages.success(request,"here")
            login(request,signed_user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = UserForm()
    context={'form':form}
    return render(request,'accounts/signupform.html',context)