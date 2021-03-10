from django.shortcuts import render, redirect
from django.template import Template
from django.http import HttpResponse

from .forms import OrderForm
from .models import *
from django.forms import inlineformset_factory

from .filters import OrderFilter


# Create your views here.

def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})



def dashboard(request):
    customer = Customer.objects.all()
    order = Order.objects.all()
    t_orders = order.count()
    p_orders = order.filter(status='Pending').count()
    d_orders = order.filter(status='Delivered').count()
    in_orders = order.filter(status='in Progress').count()
    out_orders = order.filter(status='out of order').count()

    context =  {
        'customer':customer,
        'order': order,
        't_orders': t_orders,
        'p_orders': p_orders,
        'd_orders': d_orders,
        'in_orders': in_orders,
        'out_orders': out_orders,
    }

    return render(request, 'dashboard.html', context)

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    num_orders = orders.count()

    context = {
        'customer': customer,
        'order': orders,
        'num_orders': num_orders,
    }

    return render(request, 'customer.html', context)


# def create(request):
#     form = OrderForm()
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/dash')
#
#     return render(request, 'include/form.html', {'form': form})


def create(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('book', 'status'),extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet( queryset=Order.objects.none(), instance=customer)
    #form = OrderForm()
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/dash')

    return render(request, 'include/form.html', {'formset': formset})


def update(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/dash')

    return render(request, 'include/form.html', {'form': form})


def delete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/dash')

    return render(request, 'include/delete_form.html', { 'order': order})