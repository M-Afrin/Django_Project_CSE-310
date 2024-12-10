from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request, 'Home.html')

def SignUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different username.')
            return render(request, 'signup.html')

       
        user = User.objects.create_user(username=username, email=email, password=password)

        
        request.session['signup_username'] = username
        request.session['signup_email'] = email
        request.session['signup_password'] = password

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('login')  
        else:
            messages.error(request, 'An error occurred while signing up. Please try again.')
            return render(request, 'Signup.html')
        
    return render(request, 'Signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the login credentials belong to a regular user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')  # Redirect to the booking page
         
        else:
            # Authentication failed, display an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')

@login_required
def logout(request):
    django_logout(request)
    return redirect('home')

@login_required
def user_profile(request):
    user = request.user
    try:
        user_profile = user.profile  
    except UserProfile.DoesNotExist:
        
        user_profile = None

    
    products = Product.objects.filter(seller=user) if user_profile else None

    
    orders = Order.objects.filter(user=user) if user_profile else None

    return render(request, 'user_profile.html', {
        'user': user,
        'user_profile': user_profile,
        'products': products,
        'orders': orders
    })


@login_required
def edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')

    return render(request, 'edit_profile.html', {'profile': profile})


@login_required
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        # Validate required fields
        if not all([name, description, price, category, stock]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('create_product')  

        try:
            price = float(price)  
            stock = int(stock)  
            user = request.user  

            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                stock=stock,
                image=image,
                seller=user,
            )
            messages.success(request, 'Product created successfully!')
            return redirect('user_profile')
        except ValueError:
            messages.error(request, 'Invalid price or stock value.')
            return redirect('create_product')  

    return render(request, 'create_product.html')


@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)
        product.price = request.POST.get('price', product.price)
        product.category = request.POST.get('category', product.category)
        product.stock = request.POST.get('stock', product.stock)

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        try:
            product.price = float(product.price)  
            product.stock = int(product.stock)  
            product.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('user_profile')
        except ValueError:
            messages.error(request, 'Invalid price or stock value.')
            return redirect('update_product', product_id=product.id)

    return render(request, 'update_product.html', {'product': product})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('user_profile')

    return render(request, 'delete_product.html', {'product': product})


@login_required
def seller_products(request):
    products = Product.objects.filter(seller=request.user.profile)
    return render(request, 'seller_products.html', {'products': products})


def shop(request):
    # Get the category filter from the query parameters
    category_filter = request.GET.get('category', None)

    # Filter products based on category if provided, otherwise fetch all products
    if category_filter:
        products = Product.objects.filter(category=category_filter, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    # Fetch all unique categories for the filter dropdown
    categories = Product.CATEGORY_CHOICES

    return render(request, 'shop.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_filter,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

    if not created:
        # If the item already exists, increase the quantity
        if product.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"{product.name} quantity increased.")
        else:
            messages.warning(request, "Insufficient stock available.")
    else:
        messages.success(request, f"{product.name} added to cart.")

    return redirect('cart')

@login_required(login_url='login')
def cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    # Calculate the total price of items in the cart 
    total_price = cart_items.aggregate(
        total_price=Sum(F('quantity') * F('product__price'))
    )['total_price'] or 0

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def update_cart_item(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)

    if action == 'increase':
        if cart_item.product.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"Increased quantity of {cart_item.product.name}.")
        else:
            messages.warning(request, "Insufficient stock available.")
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, f"Decreased quantity of {cart_item.product.name}.")
        else:
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.product.name} from cart.")
    elif action == 'remove':
        cart_item.delete()
        messages.success(request, f"Removed {cart_item.product.name} from cart.")

    return redirect('cart')

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    # Calculate the total price
    total_price = sum(item.get_total_price() for item in cart_items)

    # Validate stock availability for all items
    for item in cart_items:
        if item.product.stock < item.quantity:
            messages.error(
                request,
                f"Insufficient stock for {item.product.name}. Please adjust your cart.",
            )
            return redirect('cart')

    # Create the order
    order = Order.objects.create(user=user, total_price=total_price)

    # Add order items and reduce product stock
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.get_total_price(),
        )
        item.product.stock -= item.quantity
        if item.product.stock == 0:
            item.product.is_available = False
        item.product.save()

    # Clear the user's cart
    cart_items.delete()

    messages.success(request, f"Order placed successfully! Order ID: {order.id}")
    return redirect('confirm_order', order_id=order.id)

@login_required(login_url='login')
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'confirm_order.html', {'order': order})

@login_required(login_url='login')
def orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).prefetch_related('items__product')

    return render(request, 'orders.html', {'orders': orders})

@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'Pending':
        # Restore the stock of the products in the order
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        
        # Delete the order
        order.delete()
        messages.success(request, 'Order canceled successfully.')
    else:
        messages.error(request, 'Only pending orders can be canceled.')

    return redirect('orders')
        
    

def About(request):
    return render(request, 'About.html')

def Contact(request):
    return render(request, 'Contact.html')