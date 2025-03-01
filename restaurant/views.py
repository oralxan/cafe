import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import MenuItem, Review, Category, Order, OrderItem

def home(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})

def menu(request):
    category_name = request.GET.get('category')
    if category_name:
        items = MenuItem.objects.filter(category__name=category_name)
    else:
        items = MenuItem.objects.all()
    categories = Category.objects.all()
    return render(request, 'menu.html', {'items': items, 'categories': categories})

def contact(request):
    categories = Category.objects.all()
    return render(request, 'contact.html', {'categories': categories})

def reviews(request):
    all_reviews = Review.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'reviews.html', {'reviews': all_reviews, 'categories': categories})

def orders_view(request):
    orders = Order.objects.prefetch_related('orderitem_set__menu_item').all().order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})

@require_POST
def add_to_order(request):
    try:
        data = json.loads(request.body)
        item_id = data.get("item_id")

        # Get customer details from the session
        customer_email = request.session.get("customer_email")
        customer_phone = request.session.get("customer_phone")
        customer_address = request.session.get("customer_address")
        
        # If customer details are missing, ask for them
        if not (customer_email and customer_phone and customer_address):
            return JsonResponse({
                "status": "need_info",
                "message": "Please enter your email, phone, and address."
            })

        # Get the selected menu item
        menu_item = MenuItem.objects.get(id=item_id)

        # Create or get the order for the current customer
        order, created = Order.objects.get_or_create(
            customer_name="Guest",
            email=customer_email,
            phone=customer_phone,
            address=customer_address,
            defaults={'total_price': 0}
        )

        # Add the item to the order (or update quantity if it already exists)
        order_item, item_created = OrderItem.objects.get_or_create(
            order=order,
            menu_item=menu_item,
            defaults={'quantity': 1, 'price': menu_item.price}
        )

        if not item_created:
            order_item.quantity += 1
            order_item.save()

        # Update the total price of the order
        order.total_price += menu_item.price
        order.save()

        return JsonResponse({"status": "success"})
    except MenuItem.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@require_POST
def save_customer_info(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        phone = data.get("phone")
        address = data.get("address")
        
        request.session["customer_email"] = email
        request.session["customer_phone"] = phone
        request.session["customer_address"] = address
        
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@require_POST
def delete_order(request):
    try:
        data = json.loads(request.body)
        order_id = data.get("order_id")
        order = Order.objects.get(id=order_id)
        order.delete()
        return JsonResponse({"status": "success"})
    except Order.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Order not found."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
