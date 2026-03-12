from django.contrib import admin
from .models import Category, Product, CartItem, Order, OrderItem
from django.utils.html import mark_safe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Product)
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

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'added_at']
    search_fields = ['user__username', 'product__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    search_fields = ['user__username', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__id', 'product__name']
