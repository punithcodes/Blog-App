from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, PostForm
from django.contrib import messages
from .models import post
from django.contrib.auth.models import Group


# Create your views here.
def home(request):
    posts = post.objects.all()
    return render(request, 'home.html', {'posts': posts})


def about(request):
    return render(request, 'about.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts = post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'dashboard.html', {'posts': posts, 'fullname': full_name, 'groups': gps})
    else:
        return redirect('login')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created successfully !')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Success !')
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'addpost.html', {'form': form})
    else:
        return redirect('login')


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'updatepost.html', {'form': form})
    else:
        return redirect('login')


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = post.objects.get(pk=id)
            pi.delete()
            return redirect('dashboard')
    else:
        return redirect('login')


