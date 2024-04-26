from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Product, Category
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm

def category(request, foo):
    # Replace hyphens with spaces
    foo = foo.replace("-", " ")

    # Grab category from URL
    try:
        # Looks up category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(
            request, "category.html", {"products": products, "category": category}
        )
    except:
        messages.success(request, ("That category doesn't exist... Yet."))
        return redirect("home")
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request, "category_summary.html", {"categories": categories})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "product.html", {"product": product})

def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})

def about(request):
    products = Product.objects.all()
    return render(request, "about.html", {})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in."))
            return redirect("home")
        else:
            messages.success(request, ("Check your username/password."))
            return redirect("login")
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logged out."))
    return redirect("home")

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            # Log In User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered successfully."))
            return redirect("home")
        else:
            messages.success(
                request, ("There was an issue registering. Please try again.")
            )
            return redirect("register")
    else:
        return render(request, "register.html", {"form": form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Profile has been updated.")
            return redirect("home")
        return render(request, "update_user.html", {"user_form":user_form})
    else:
        messages.success(request,"You must be logged in to update profile.")
        return redirect("home")
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        # Verifies if user filled out form
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)

            # Is form valid
            if form.is_valid():
                form.save()
                messages.success(request,"Your password has been updated.")
                login(request, current_user)
                return redirect("update_user")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {"form":form})
    else:
            messages.success(request, "You must be logged in to update password.")