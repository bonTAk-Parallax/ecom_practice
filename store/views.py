from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import  RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


# def register_request(request):
#     if request.method == 'POST':
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Registration Successful.")
#             return HttpResponseRedirect(reverse("store:homepage"))
#         messages.error(request, "Could not register!")
#     form = NewUserForm()
#     return render(request=request, template_name="store/register.html", context={'register_form': form})

def register_request(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful.")
            return HttpResponseRedirect(reverse("store:homepage"))
        print(form.errors)
        messages.error(request, "Could not register!")
    form = RegisterForm()
    return render(request=request, template_name="store/register.html", context={'form': form})


# def login_request(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data = request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 print(request.user.is_authenticated)
#                 messages.info(request, f"You are now logged in as {username}.")
#                 return HttpResponseRedirect(reverse("store:homepage"))
#             else:
#                 messages.error(request, "Invalid username or password!")
#         else:
#             messages.error(request, "Invalid username or password")
#     form = AuthenticationForm()
#     return render(request, "store/login.html", {'login_form': form})


def login_request(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("store:homepage"))
        else:
            return render(request, "store/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "store/login.html")



def logout_request(request):
    logout(request)
    messages.info(request, "You have looged out.")
    return HttpResponseRedirect(reverse("store:homepage"))


def homepage(request):
    # products = Product.objects.all()
    # return render(request, "store/homepage.html", {"products": products})

    product_list = Product.objects.all()
    paginator = Paginator(product_list, 3)  
    page_number = request.GET.get("page", 1)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, "store/homepage.html", {"products": products})



def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print("DETAILS LOADING....")
    return render(request, "store/product_detail.html", {"product": product})


def search(request):
    # p_name = request.GET.get('content')
    # print(p_name)
    # result = Product.objects.get(name__icontains = p_name)
    # print(result)
    # return render(request, "store/product_detail.html", {"product": result})

    p_name = request.GET.get('content')
    print(p_name)
    results = Product.objects.filter(name__icontains = p_name)
    print(results)
    return render(request, "store/product_detail.html", {"products": results})




def cart(request, pk):
    print(pk)
    item = Product.objects.get(pk=pk)
    order, created = Order.objects.get_or_create(customer = request.user, complete = False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, item = item)
    orderitem.add_to_cart()
    print(orderitem.price)
    return redirect('store:homepage')

def checkout(request):
    user = request.user
    order = Order.objects.get(customer=user)
    order_items = order.orderitem_set.filter()
    print(order_items)
    return render(request, 'store/checkout.html', {'order': order, "order_items": order_items})


def cancel(request, pk):
    order = Order.objects.get(pk=pk)
    order.rollback()
    return HttpResponseRedirect(reverse('store:homepage'))


def confirm(self):
    return HttpResponse("ORDER SUCCESSFULL!")


    


