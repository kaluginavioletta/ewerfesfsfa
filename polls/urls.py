from django.urls import path
from . import views

from .views import ProductLoginView, ProductLogoutView, ProductLogoutView, profile, RegisterUserView

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', profile, name='profile'),
    path('service/<int:id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', ProductLoginView.as_view(), name='login'),
    path('logout/', ProductLogoutView.as_view(), name='logout'),
    path('service/', views.all_products, name='service'),
]
