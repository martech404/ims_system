from django.shortcuts import redirect
from django.contrib import messages

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.role in ['admin', 'manager']:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, "You are not authorized to view that page.")
            return redirect('pos_view')  # Send unauthorized users to POS
    return wrapper_func

def cashier_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.role == 'cashier':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('dashboard')
    return wrapper_func