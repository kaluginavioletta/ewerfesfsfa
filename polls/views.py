from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.db.models.functions import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Product, User, Order
from django.urls import reverse
from django.views import generic
from .forms import RegisterUserForm, OrderForm
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


def index(request):
    products_requests = Product.objects.order_by('-pub_date')[:5]
    return render(request, 'index.html', {'products_requests': products_requests})


@login_required
def profile(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user)
    context = {'orders': orders}
    return render(request, 'main/profile.html', context)

class ProductDetailView(generic.DetailView):
    pk_url_kwarg = 'id'
    model = Product
    template_name = 'products/product_detail.html'
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            product = self.get_object()
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.save()
            messages.success(request, 'Товар/услуга успешно заказан!')
            return redirect('polls:profile', id=product.id)
        else:
            messages.error(request, 'Ошибка заказа товара/услуги.')
            return self.get(request, *args, **kwargs)


def all_products(request):
    product_requests = Product.objects.all()
    return render(request, 'products/all_products.html', {'product_requests': product_requests})





class ProductLoginView(LoginView):
    template_name = 'main/login.html'


class ProductLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('polls:profile')


def search_view(request):
    query = request.GET.get('query')
    results = []

    if query:
        results = Product.objects.filter(title__icontains=query)

    context = {'results': results}
    return render(request, 'products/search_result.html', context)
