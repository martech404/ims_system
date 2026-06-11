from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from users.decorators import admin_only
from inventory.models import Product


@login_required
def dashboard(request):
    # If a cashier tries to access dashboard, send them to POS
    if request.user.role == 'cashier':
        return redirect('pos_view')

    # If admin/manager, show the dashboard
    total_products = Product.objects.count()
    low_stock = Product.objects.filter(quantity__lte=5).count()

    context = {
        'total_products': total_products,
        'low_stock': low_stock,
    }
    return render(request, 'dashboard.html', context)

def custom_logout(request):
    logout(request)
    return redirect('login')