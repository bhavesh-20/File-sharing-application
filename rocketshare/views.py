from django.shortcuts import render,reverse,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate


# Create your views here.
def index(request):
    return  render(request,'rocketshare/index.html')

def signup(request):
    if request.method  == "GET":
        return render(request,'rocketshare/signup.html')
    else:
        username, password1, password2 = request.POST['username'], request.POST['password1'], request.POST['password2']
        user = User.objects.create_user(username = username, password = password1)
        user.save()
        login(request,user)
        return redirect(reverse('index'))

def signout(request):
    logout(request)
    return redirect(reverse('signup'))

def signin(request):
    if request.method  == "GET":
        return render(request,'rocketshare/login.html')
    else:
        username, password= request.POST['username'], request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect(reverse('index'))
        else:
            return HttpResponse("Invalid Credentials")