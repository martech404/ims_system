from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from inventory.models import Product
from django.db import transaction
from .models import Sale, SaleItem
from django.db.models import Sum
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
from users.decorators import admin_only
import json

@login_required
def pos_view(request):
    products = Product.objects.filter(quantity__gt=0).order_by('name')

    if request.method == 'POST':
        cart_data = request.POST.get('cart_data', '{}')
        try:
            cart = json.loads(cart_data)
        except json.JSONDecodeError:
            cart = {}

        if not cart:
            context = {'products': products, 'error': 'Cart is empty'}
            return render(request, 'sales/pos.html', context)

        try:
            with transaction.atomic():
                sale = Sale.objects.create(
                    cashier=request.user,
                    total_amount=0
                )

                grand_total = 0

                for product_id, item in cart.items():
                    product = Product.objects.select_for_update().get(id=int(product_id))

                    if product.quantity < item['qty']:
                        raise ValueError(f"Insufficient stock for {product.name}")

                    product.quantity -= item['qty']
                    product.save()

                    SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        price=product.price,
                        quantity=item['qty']
                    )

                    grand_total += product.price * item['qty']

                sale.total_amount = grand_total
                sale.save()

            # Redirect to receipt page after successful sale
            return redirect('receipt', sale_id=sale.id)

        except Product.DoesNotExist:
            context = {'products': products, 'error': 'A product was not found'}
            return render(request, 'sales/pos.html', context)
        except ValueError as e:
            context = {'products': products, 'error': str(e)}
            return render(request, 'sales/pos.html', context)

    context = {'products': products}
    return render(request, 'sales/pos.html', context)
@login_required
def report_view(request):
    total_revenue = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_sales_count = Sale.objects.count()
    recent_sales = Sale.objects.select_related('cashier').order_by('-date_added')[:10]

    today = timezone.now().date()
    last_7_days = today - timedelta(days=6)

    daily_sales = Sale.objects.filter(date_added__date__gte=last_7_days) \
        .annotate(date=TruncDate('date_added')) \
        .values('date') \
        .annotate(daily_total=Sum('total_amount')) \
        .order_by('date')

    import json as json_module
    dates = [sale['date'].strftime('%Y-%m-%d') for sale in daily_sales]
    amounts = [float(sale['daily_total']) for sale in daily_sales]

    context = {
        'total_revenue': total_revenue,
        'total_sales_count': total_sales_count,
        'recent_sales': recent_sales,
        'chart_dates': json_module.dumps(dates),
        'chart_amounts': json_module.dumps(amounts),
    }
    return render(request, 'sales/report.html', context)


@login_required
def receipt_view(request, sale_id):
    from django.shortcuts import get_object_or_404
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'sales/receipt.html', {'sale': sale})
