from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Product, Category, CartItem, Order, OrderItem
from django.contrib import messages
from django.http import JsonResponse

# Home Page
def home(request):
    """Trang chủ - Hiển thị danh sách sản phẩm"""
    products = Product.objects.filter(status='available')[:8]
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'page_title': 'Home'
    }
    return render(request, 'shop/home.html', context)


# Product Pages
def product_list(request):
    """Danh sách sản phẩm với tìm kiếm và lọc"""
    products = Product.objects.filter(status='available')
    categories = Category.objects.all()
    
    # Tìm kiếm
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    # Lọc theo danh mục
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Lọc theo giá
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    
    context = {
        'products': products,
        'categories': categories,
        'page_title': 'Products'
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """Chi tiết sản phẩm"""
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(
        category=product.category,
        status='available'
    ).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'page_title': product.name
    }
    return render(request, 'shop/product_detail.html', context)


# Authentication
def register(request):
    """Đăng ký tài khoản"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')
        
        # Kiểm tra mật khẩu không hợp lệ
        from django.contrib.auth.password_validation import validate_password, ValidationError
        try:
            validate_password(password1, user=User(username=username, email=email))
        except ValidationError as e:
            for err in e.messages:
                messages.error(request, err)
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'shop/register.html', {'page_title': 'Register'})


def login_view(request):
    """Đăng nhập"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')
    
    return render(request, 'shop/login.html', {'page_title': 'Login'})


def logout_view(request):
    """Đăng xuất"""
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')


# Cart & Order
@login_required(login_url='login')
def cart(request):
    """Giỏ hàng"""
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.discount_price or item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'page_title': 'Shopping Cart'
    }
    return render(request, 'shop/cart.html', context)


@login_required(login_url='login')
@require_POST
def add_to_cart(request):
    """Thêm vào giỏ hàng"""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    cart_item.save()
    messages.success(request, f'{product.name} added to cart!')
    return redirect('product_detail', pk=product_id)


@login_required(login_url='login')
@require_POST
def remove_from_cart(request, pk):
    """Xóa khỏi giỏ hàng"""
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    """Thanh toán"""
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('product_list')
    
    total_amount = sum(item.product.discount_price or item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        phone_number = request.POST.get('phone_number')
        
        # Tạo đơn hàng
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            delivery_address=delivery_address,
            phone_number=phone_number
        )
        
        # Tạo chi tiết đơn hàng
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discount_price or item.product.price
            )
        
        # Xóa giỏ hàng
        cart_items.delete()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('order_detail', pk=order.id)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'page_title': 'Checkout'
    }
    return render(request, 'shop/checkout.html', context)


@login_required(login_url='login')
def order_list(request):
    """Danh sách đơn hàng"""
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
        'page_title': 'My Orders'
    }
    return render(request, 'shop/order_list.html', context)


@login_required(login_url='login')
def order_detail(request, pk):
    """Chi tiết đơn hàng"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    order_items = order.order_items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
        'page_title': f'Order {order.id}'
    }
    return render(request, 'shop/order_detail.html', context)


# Dashboard
@login_required(login_url='login')
def dashboard(request):
    """Dashboard người dùng"""
    orders = Order.objects.filter(user=request.user).count()
    total_spent = sum(o.total_amount for o in Order.objects.filter(user=request.user))
    
    context = {
        'orders_count': orders,
        'total_spent': total_spent,
        'page_title': 'Dashboard'
    }
    return render(request, 'shop/dashboard.html', context)
