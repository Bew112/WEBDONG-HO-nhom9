from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Brand(models.Model):
    """Thương hiệu đồng hồ"""
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=50, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Brands"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Danh mục sản phẩm"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Sản phẩm đồng hồ"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold_out', 'Sold Out'),
        ('discontinued', 'Discontinued'),
        ('pre_order', 'Pre-order'),
    ]
    
    name = models.CharField(max_length=300)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Giá sau chiết khấu. Phải nhỏ hơn giá gốc."
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True)
    warranty_months = models.IntegerField(default=12, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['brand', 'name'],
                name='unique_brand_product_name'
            )
        ]
    
    def __str__(self):
        return self.name
    
    def get_discount_percentage(self):
        if self.discount_price and self.discount_price < self.price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return int(discount)
        return 0
    
    def get_current_price(self):
        return self.discount_price if self.discount_price else self.price


class ProductRating(models.Model):
    """Đánh giá & bình luận sản phẩm"""
    RATING_CHOICES = [
        (1, '⭐ 1 sao'),
        (2, '⭐⭐ 2 sao'),
        (3, '⭐⭐⭐ 3 sao'),
        (4, '⭐⭐⭐⭐ 4 sao'),
        (5, '⭐⭐⭐⭐⭐ 5 sao'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_ratings')
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']
        verbose_name_plural = "Product Ratings"
    
    def __str__(self):
        return f"{self.product.name} - {self.rating} sao từ {self.user.username}"


class CartItem(models.Model):
    """Mục trong giỏ hàng"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity})"
    
    def get_total_price(self):
        return self.product.get_current_price() * self.quantity


class Order(models.Model):
    """Đơn hàng"""
    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy'),
        ('returned', 'Đã hoàn trả'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(
        max_length=20,
        choices=[('cod', 'COD'), ('bank_transfer', 'Chuyển khoản ngân hàng')],
        default='cod'
    )
    payment_reference = models.CharField(max_length=100, blank=True)
    delivery_address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    """Chi tiết đơn hàng"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        unique_together = ['order', 'product']
    
    def __str__(self):
        return f"Đơn hàng #{self.order.id} - {self.product.name} (x{self.quantity})"
    
    def get_subtotal(self):
        return self.price * self.quantity


class Shipment(models.Model):
    """Thông tin vận chuyển đơn hàng"""
    STATUS_CHOICES = [
        ('pending', 'Chờ lấy hàng'),
        ('picked_up', 'Đã lấy hàng'),
        ('in_transit', 'Đang vận chuyển'),
        ('out_for_delivery', 'Sắp giao'),
        ('delivered', 'Đã giao'),
        ('failed', 'Giao thất bại'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipment')
    carrier = models.CharField(max_length=100, help_text="Hãng vận chuyển (ViettelPost, GHN, ...)")
    tracking_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Vận chuyển #{self.tracking_number} - Đơn hàng #{self.order.id}"

