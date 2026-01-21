from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("store/", views.homepage, name="homepage"),
    path("register/", views.register_request, name='register'),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    path('store/<int:pk>/', views.detail, name="detail"),
    path('search/', views.search, name="search"),
    path('cart/<int:pk>', views.cart, name="cart"),
]