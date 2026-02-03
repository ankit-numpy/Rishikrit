from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CheckoutForm
from .models import Order, OrderItem, Product


def _get_cart(session):
    return session.setdefault("cart", {})


def home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "store/home.html", {"products": products})


def cart_detail(request):
    cart = _get_cart(request.session)
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids, is_active=True)
    items = []
    subtotal = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        line_total = product.price * quantity
        subtotal += line_total
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "line_total": line_total,
            }
        )
    return render(
        request,
        "store/cart.html",
        {
            "items": items,
            "subtotal": subtotal,
        },
    )


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_cart(request.session)
    current_qty = cart.get(str(product.id), 0)
    if product.inventory <= current_qty:
        messages.warning(request, "Not enough stock available for this item.")
        return redirect("store:cart")
    cart[str(product.id)] = current_qty + 1
    request.session.modified = True
    messages.success(request, f"{product.name} added to your cart.")
    return redirect("store:cart")


def remove_from_cart(request, product_id):
    cart = _get_cart(request.session)
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session.modified = True
    return redirect("store:cart")


def update_cart(request, product_id):
    if request.method != "POST":
        return redirect("store:cart")
    cart = _get_cart(request.session)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1
    quantity = max(1, quantity)
    if quantity > product.inventory:
        messages.warning(request, "Requested quantity exceeds available stock.")
        quantity = product.inventory
    cart[str(product.id)] = quantity
    request.session.modified = True
    return redirect("store:cart")


def checkout(request):
    cart = _get_cart(request.session)
    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect("store:home")

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids, is_active=True)
    items = []
    subtotal = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        line_total = product.price * quantity
        subtotal += line_total
        items.append({"product": product, "quantity": quantity, "line_total": line_total})

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(**form.cleaned_data)
                for item in items:
                    product = item["product"]
                    quantity = item["quantity"]
                    if product.inventory < quantity:
                        messages.warning(
                            request,
                            f"Only {product.inventory} units left for {product.name}.",
                        )
                        return redirect("store:cart")
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                    )
                    product.inventory -= quantity
                    product.save(update_fields=["inventory"])
            request.session["cart"] = {}
            messages.success(request, "Your order has been placed successfully!")
            return redirect(reverse("store:order_success", kwargs={"order_id": order.id}))
    else:
        form = CheckoutForm()

    return render(
        request,
        "store/checkout.html",
        {"items": items, "subtotal": subtotal, "form": form},
    )


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "store/order_success.html", {"order": order})
