import json
from datetime import timedelta

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Category, Product, CartItem, Order, OrderItem
from django.utils.html import mark_safe
from django.db.models import Sum

# Custom Admin Site
class WatchShopAdminSite(AdminSite):
    site_header = "👨‍💼 Watch Shop Admin Dashboard"
    site_title = "Watch Shop Admin"
    index_title = "Quản Lý Cửa Hàng"
    
    def index(self, request, extra_context=None):
        """Custom dashboard cho admin"""
        from django.db.models import Sum
        from django.contrib.auth.models import User as DjangoUser
        from .models import Order, Product
        
        # Thống kê
        all_orders = Order.objects.all()
        pending_orders = all_orders.filter(status='pending')
        approved_orders = all_orders.filter(status='approved')
        rejected_orders = all_orders.filter(status='rejected')
        
        total_revenue = all_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        pending_revenue = pending_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Data for charts
        today = timezone.localdate()
        dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        trend_labels = [d.strftime('%d/%m') for d in dates]
        trend_data = [all_orders.filter(created_at__date=d).count() for d in dates]

        status_labels = ['Chờ Xử Lý', 'Đã Duyệt', 'Từ Chối']
        status_data = [pending_orders.count(), approved_orders.count(), rejected_orders.count()]

        extra_context = extra_context or {}
        extra_context.update({
            'total_orders': all_orders.count(),
            'pending_orders': pending_orders.count(),
            'approved_orders': approved_orders.count(),
            'rejected_orders': rejected_orders.count(),
            'total_revenue': total_revenue,
            'pending_revenue': pending_revenue,
            'total_products': Product.objects.count(),
            'total_users': DjangoUser.objects.count(),
            'available_products': Product.objects.filter(status='available').count(),
            'recent_orders': all_orders.order_by('-created_at')[:10],
            'recent_users': DjangoUser.objects.all().order_by('-date_joined')[:10],
            'orders_trend_chart': json.dumps({'labels': trend_labels, 'data': trend_data}),
            'orders_status_chart': json.dumps({'labels': status_labels, 'data': status_data}),
        })
        
        return super().index(request, extra_context)

# Tạo instance custom admin site
admin_site = WatchShopAdminSite()

# Model Admins
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height:60px; max-width:60px; border-radius:6px;" />')
        return "Không có ảnh"
    image_tag.short_description = 'Ảnh'

    def discount_percent(self, obj):
        if obj.discount_price and obj.discount_price < obj.price:
            return int(round((obj.price - obj.discount_price) / obj.price * 100))
        return 0
    discount_percent.short_description = 'Giảm giá (%)'

    def price_after_discount(self, obj):
        if obj.discount_price and obj.discount_price < obj.price:
            return obj.discount_price
        return '-'
    price_after_discount.short_description = 'Giá sau giảm'

    def is_available(self, obj):
        return obj.status == 'available'
    is_available.boolean = True
    is_available.short_description = 'Có sẵn'

    list_display = ['image_tag', 'name', 'category', 'price', 'discount_percent', 'price_after_discount', 'stock', 'is_available', 'created_at']
    search_fields = ['name']
    autocomplete_fields = ['category']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['category', 'status', 'created_at']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'added_at']
    search_fields = ['user__username', 'product__name']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    search_fields = ['user__username', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__id', 'product__name']


# Register with custom admin site
admin_site.register(Category, CategoryAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(CartItem, CartItemAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(OrderItem, OrderItemAdmin)
