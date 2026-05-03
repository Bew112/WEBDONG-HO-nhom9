import io

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Avg, Sum, Count, F
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Product, Category, CartItem, Order, OrderItem, Brand, ProductRating, Shipment
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from datetime import timedelta, datetime
from django.utils import timezone
import json

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
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
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
from .forms import RegistrationForm


def register(request):
    """Đăng ký tài khoản"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('register')

    form = RegistrationForm()
    return render(request, 'shop/register.html', {'form': form, 'page_title': 'Register'})


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
    total = sum((item.product.discount_price or item.product.price) * item.quantity for item in cart_items)
    
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
def buy_now(request):
    """Mua ngay sản phẩm mà không qua trang giỏ hàng"""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, pk=product_id)

    if product.status != 'available':
        messages.error(request, 'Sản phẩm hiện không thể mua ngay.')
        return redirect('product_detail', pk=product_id)

    return redirect(f"{reverse('checkout')}?buy_now_product_id={product.id}&buy_now_quantity={quantity}")


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
    buy_now_items = None
    buy_now_product_id_post = request.POST.get('buy_now_product_id')
    buy_now_quantity_post = int(request.POST.get('buy_now_quantity', 1)) if request.POST.get('buy_now_quantity') else 1
    buy_now_product_id_get = request.GET.get('buy_now_product_id')
    buy_now_quantity_get = int(request.GET.get('buy_now_quantity', 1)) if request.GET.get('buy_now_quantity') else 1

    if request.method == 'GET':
        if buy_now_product_id_get:
            product = get_object_or_404(Product, pk=buy_now_product_id_get)
            buy_now_items = [{'product': product, 'quantity': buy_now_quantity_get}]
            total_amount = (product.discount_price or product.price) * buy_now_quantity_get
        else:
            if not cart_items.exists():
                messages.error(request, 'Your cart is empty!')
                return redirect('product_list')
            total_amount = sum((item.product.discount_price or item.product.price) * item.quantity for item in cart_items)

    elif request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        phone_number = request.POST.get('phone_number')
        payment_method = request.POST.get('payment', 'cod')

        if buy_now_product_id_post:
            product = get_object_or_404(Product, pk=buy_now_product_id_post)
            quantity = buy_now_quantity_post
            order = Order.objects.create(
                user=request.user,
                total_amount=(product.discount_price or product.price) * quantity,
                delivery_address=delivery_address,
                phone_number=phone_number,
                payment_method=payment_method,
            )
            if payment_method == 'bank_transfer':
                order.payment_reference = f"TT{order.id:06d}"
                order.save()
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.discount_price or product.price
            )
            buy_now_items = [{'product': product, 'quantity': quantity}]
            total_amount = (product.discount_price or product.price) * quantity
        else:
            if not cart_items.exists():
                messages.error(request, 'Your cart is empty!')
                return redirect('cart')
            total_amount = sum((item.product.discount_price or item.product.price) * item.quantity for item in cart_items)
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                delivery_address=delivery_address,
                phone_number=phone_number,
                payment_method=payment_method,
            )
            if payment_method == 'bank_transfer':
                order.payment_reference = f"TT{order.id:06d}"
                order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.discount_price or item.product.price
                )
            cart_items.delete()

        messages.success(request, 'Order placed successfully!')
        return redirect('order_detail', pk=order.id)

    context = {
        'cart_items': cart_items,
        'buy_now_items': buy_now_items,
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


@login_required(login_url='login')
def order_payment_qr(request, pk):
    """Trả về QR code cho đơn hàng chuyển khoản"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.payment_method != 'bank_transfer':
        return HttpResponse(status=404)

    payload = (
        f"VietinBank;CN THAI NGUYEN - HOI SO;BANNAVONG SOUKSAVANH;"
        f"107877332500;SOTIEN:{order.total_amount:.0f};NOIDUNG:{order.payment_reference}"
    )
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=3,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        fill_color='black',
        back_color='white'
    )
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')


# ============= THỐNG KÊ & BÁO CÁO =============

def statistics_dashboard(request):
    """Dashboard thống kê tổng hợp"""
    today = timezone.now().date()
    days_ago_7 = today - timedelta(days=7)
    days_ago_30 = today - timedelta(days=30)
    
    # Tổng quan
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_products = Product.objects.count()
    total_customers = Order.objects.values('user').distinct().count()
    
    # Đơn hàng theo trạng thái
    order_status = {
        'pending': Order.objects.filter(status='pending').count(),
        'confirmed': Order.objects.filter(status='confirmed').count(),
        'shipping': Order.objects.filter(status='shipping').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }
    
    # Doanh thu 7 ngày gần đây
    dates_7 = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    revenue_7 = []
    for d in dates_7:
        date_obj = datetime.fromisoformat(d).date()
        revenue = Order.objects.filter(created_at__date=date_obj).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        revenue_7.append(float(revenue))
    
    # Doanh thu theo danh mục
    categories_data = Category.objects.annotate(
        total_revenue=Sum('products__order_items__price')
    ).values('name', 'total_revenue').filter(total_revenue__isnull=False).order_by('-total_revenue')[:5]
    
    category_names = [cat['name'] for cat in categories_data]
    category_revenues = [float(cat['total_revenue'] or 0) for cat in categories_data]
    
    # Sản phẩm bán chạy
    top_products = Product.objects.annotate(
        total_sold=Sum('order_items__quantity'),
        total_revenue=Sum(F('order_items__price') * F('order_items__quantity'))
    ).filter(total_sold__isnull=False).order_by('-total_revenue')[:5]
    
    # Đơn hàng 7 ngày gần đây
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    
    context = {
        'total_orders': total_orders,
        'total_revenue': int(total_revenue),
        'total_products': total_products,
        'total_customers': total_customers,
        'order_status': order_status,
        'dates_7': json.dumps(dates_7),
        'revenue_7': json.dumps(revenue_7),
        'category_names': json.dumps(category_names),
        'category_revenues': json.dumps(category_revenues),
        'top_products': top_products,
        'recent_orders': recent_orders,
        'page_title': 'Dashboard Thống Kê'
    }
    return render(request, 'shop/statistics.html', context)


def revenue_report(request):
    """Báo cáo doanh thu theo ngày/tháng"""
    report_type = request.GET.get('type', 'daily')  # daily, monthly
    
    if report_type == 'monthly':
        # Báo cáo theo tháng (năm hiện tại)
        months = []
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        revenues = []
        
        today = timezone.now()
        for month in range(1, today.month + 1):
            first_day = today.replace(month=month, day=1)
            if month == today.month:
                last_day = today.date()
            else:
                last_day = (first_day.replace(month=month + 1, day=1) - timedelta(days=1)).date()
            
            revenue = Order.objects.filter(
                created_at__date__gte=first_day.date(),
                created_at__date__lte=last_day
            ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            
            months.append(month_names[month - 1])
            revenues.append(float(revenue))
        
        chart_label = 'Doanh thu theo tháng'
        x_label = 'Tháng'
    else:
        # Báo cáo theo ngày (30 ngày gần đây)
        today = timezone.now().date()
        months = []
        revenues = []
        
        for i in range(29, -1, -1):
            date = today - timedelta(days=i)
            revenue = Order.objects.filter(created_at__date=date).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            
            months.append(date.strftime('%d/%m'))
            revenues.append(float(revenue))
        
        chart_label = 'Doanh thu theo ngày (30 ngày)'
        x_label = 'Ngày'
    
    context = {
        'report_type': report_type,
        'chart_label': chart_label,
        'x_label': x_label,
        'labels': json.dumps(months),
        'revenues': json.dumps(revenues),
        'page_title': 'Báo Cáo Doanh Thu'
    }
    return render(request, 'shop/revenue_report.html', context)


def category_report(request):
    """Báo cáo doanh thu theo danh mục"""
    categories = Category.objects.annotate(
        total_revenue=Sum('products__order_items__price'),
        product_count=Count('products'),
        order_count=Count('products__order_items')
    ).filter(total_revenue__isnull=False).order_by('-total_revenue')
    
    category_names = [cat.name for cat in categories]
    category_revenues = [float(cat.total_revenue or 0) for cat in categories]
    
    context = {
        'categories': categories,
        'category_names': json.dumps(category_names),
        'category_revenues': json.dumps(category_revenues),
        'page_title': 'Báo Cáo Theo Danh Mục'
    }
    return render(request, 'shop/category_report.html', context)


def product_report(request):
    """Báo cáo sản phẩm bán chạy"""
    sort_by = request.GET.get('sort', 'revenue')  # revenue, quantity
    
    products = Product.objects.annotate(
        total_sold=Sum('order_items__quantity'),
        total_revenue=Sum(F('order_items__price') * F('order_items__quantity')),
        avg_rating=Avg('ratings__rating')
    ).filter(total_sold__isnull=False)
    
    if sort_by == 'quantity':
        products = products.order_by('-total_sold')
    else:
        products = products.order_by('-total_revenue')
    
    product_names = [p.name for p in products[:10]]
    if sort_by == 'quantity':
        product_values = [int(p.total_sold or 0) for p in products[:10]]
        value_label = 'Số Lượng Bán'
    else:
        product_values = [float(p.total_revenue or 0) for p in products[:10]]
        value_label = 'Doanh Thu'
    
    context = {
        'sort_by': sort_by,
        'products': products[:10],
        'product_names': json.dumps(product_names),
        'product_values': json.dumps(product_values),
        'value_label': value_label,
        'page_title': 'Báo Cáo Sản Phẩm Bán Chạy'
    }
    return render(request, 'shop/product_report.html', context)


def order_status_report(request):
    """Báo cáo tình trạng đơn hàng"""
    status_data = Order.objects.values('status').annotate(
        count=Count('id'),
        total_revenue=Sum('total_amount')
    ).order_by('-count')
    
    status_labels = {
        'pending': 'Chờ xác nhận',
        'confirmed': 'Đã xác nhận',
        'shipping': 'Đang giao',
        'delivered': 'Đã giao',
        'cancelled': 'Đã hủy',
        'returned': 'Hoàn trả'
    }
    
    statuses = []
    counts = []
    revenues = []
    
    for item in status_data:
        status = item['status']
        statuses.append(status_labels.get(status, status))
        counts.append(item['count'])
        revenues.append(float(item['total_revenue'] or 0))
    
    context = {
        'status_data': status_data,
        'status_labels': json.dumps(statuses),
        'status_counts': json.dumps(counts),
        'status_revenues': json.dumps(revenues),
        'page_title': 'Báo Cáo Tình Trạng Đơn Hàng'
    }
    return render(request, 'shop/order_status_report.html', context)