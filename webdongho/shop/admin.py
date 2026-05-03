import json
from datetime import timedelta

from django.contrib import admin, messages
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from django.utils import timezone
from .models import Category, Product, CartItem, Order, OrderItem, Brand, ProductRating, Shipment
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
        confirmed_orders = all_orders.filter(status='confirmed')
        delivered_orders = all_orders.filter(status='delivered')
        
        total_revenue = all_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        pending_revenue = pending_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Data for charts
        today = timezone.localdate()
        dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        trend_labels = [d.strftime('%d/%m') for d in dates]
        trend_data = [all_orders.filter(created_at__date=d).count() for d in dates]

        status_labels = ['Chờ Xác Nhận', 'Đã Xác Nhận', 'Đã Giao']
        status_data = [pending_orders.count(), confirmed_orders.count(), delivered_orders.count()]

        extra_context = extra_context or {}
        extra_context.update({
            'total_orders': all_orders.count(),
            'pending_orders': pending_orders.count(),
            'confirmed_orders': confirmed_orders.count(),
            'delivered_orders': delivered_orders.count(),
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('shop/order/<int:order_id>/confirm/', self.admin_view(self.confirm_order_view), name='shop_order_confirm'),
        ]
        return custom_urls + urls

    def confirm_order_view(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if order.status != 'pending':
            messages.warning(request, f"Đơn hàng #{order.id} không ở trạng thái chờ xác nhận.")
            return redirect(f"/admin/shop/order/{order.id}/change/")

        order.status = 'confirmed'
        order.save()
        messages.success(request, f"Đã xác nhận đơn hàng #{order.id}.")
        return redirect(f"/admin/shop/order/{order.id}/change/")

# Tạo instance custom admin site
admin_site = WatchShopAdminSite()

# Model Admins
class BrandAdmin(admin.ModelAdmin):
    def logo_tag(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" style="max-height:40px; max-width:40px; border-radius:4px;" />')
        return "Không có"
    logo_tag.short_description = 'Logo'
    
    list_display = ['logo_tag', 'name', 'country', 'founded_year', 'created_at']
    search_fields = ['name', 'country']
    readonly_fields = ['created_at']


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

    list_display = ['image_tag', 'name', 'brand', 'category', 'price', 'discount_percent', 'price_after_discount', 'stock', 'is_available', 'created_at']
    search_fields = ['name']
    autocomplete_fields = ['category', 'brand']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['brand', 'category', 'status', 'created_at']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'added_at']
    search_fields = ['user__username', 'product__name']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    search_fields = ['user__username', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    actions = ['confirm_orders']

    @admin.action(description='Xác nhận đơn hàng đã chọn')
    def confirm_orders(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        if updated:
            self.message_user(request, f"Đã xác nhận {updated} đơn hàng.", messages.SUCCESS)
        else:
            self.message_user(request, "Không có đơn hàng chờ xác nhận trong lựa chọn.", messages.WARNING)


class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['rating', 'created_at']


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'order', 'carrier', 'status', 'estimated_delivery', 'actual_delivery']
    search_fields = ['tracking_number', 'order__id']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['status', 'carrier', 'created_at']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__id', 'product__name']


# Register with custom admin site
admin_site.register(Brand, BrandAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(CartItem, CartItemAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(OrderItem, OrderItemAdmin)
admin_site.register(ProductRating, ProductRatingAdmin)
admin_site.register(Shipment, ShipmentAdmin)
