from django.shortcuts import render,reverse,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import *
import re


# Create your views here.
regex_email = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
regex_username = '^[a-zA-Z0-9_.-]+$'

def check_username(request,username: str):
    if re.match(regex_username, username) is None:
        messages.info(request,"Invalid Username")
        return False
    if User.objects.filter(username = username).exists():
        messages.info(request,"Username Taken")
        return False
    return True

def check_password(request,password1: str, password2: str):
    if password1!=password2:
        messages.info(request,"Passwords do not match")
        return False
    return True

def check_email(request,email: str):
    if re.match(regex_email, email) is None:
        messages.info(request,"Invalid email")
        return False
    if User.objects.filter(email = email).exists():
        messages.info(request,"User already exists with given email")
        return False
    return True

def find_username(request, username):
    if re.match(regex_username, username):
        return username
    elif re.match(regex_email, username):
        if User.objects.filter(email = username).exists():
            username = User.objects.get(email = username).username
            return username
        else:
            return ""
    else:
        return ""

def index(request):
    return  render(request,'rocketshare/index.html')

def signup(request):
    if request.method  == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return render(request,'rocketshare/signup.html')
    else:
        username, email, password1, password2 = request.POST['username'], request.POST['email'], request.POST['password1'], request.POST['password2']
        if check_username(request,username) and check_email(request,email) and check_password(request,password1,password2):
            user = User.objects.create_user(username = username, password = password1, email=email)
            user.save()
            login(request,user)
            return redirect(reverse('index'))
        else:
            return redirect(reverse('signup'))

def signout(request):
    logout(request)
    return redirect(reverse('login'))

def signin(request):
    if request.method  == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return render(request,'rocketshare/login.html')
    else:
        username, password= request.POST['username'], request.POST['password']
        username = find_username(request,username)
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect(reverse('index'))
        else:
            messages.info(request,"Invalid Credentials")
            return redirect(reverse('login'))

def share(request):
    if request.method == "GET":
        return render(request, 'rocketshare/share.html')
    else:
        filename, desc, file = request.POST['filename'], request.POST['description'], request.FILES['file']
        if file.size > 2 * 10**6 and not request.user.is_authenticated:
            return HttpResponse("File size exceeded, login to continue")
        newfile = SharedFile(name = filename, description = desc, actual_file = file)
        if request.user.is_authenticated:
            newfile.owner = request.user
        else:
            newfile.owner = None
        newfile.save()
        return redirect(reverse('list'))


def listfiles(request):
    if request.GET.get('search') and request.GET['search'] != '':
        files = SharedFile.objects.filter(name__icontains = request.GET['search'])
    else:
        files = SharedFile.objects.all()
    return render(request, 'rocketshare/list.html', {'files': files})