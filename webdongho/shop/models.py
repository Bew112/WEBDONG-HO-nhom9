from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

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
    BRAND_CHOICES = (
        ('Rolex', 'Rolex'),
        ('Omega', 'Omega'),
        ('Cartier', 'Cartier'),
        ('TAG Heuer', 'TAG Heuer'),
        ('Patek Philippe', 'Patek Philippe'),
        ('IWC', 'IWC'),
        ('Seiko', 'Seiko'),
        ('Casio', 'Casio'),
        ('Orient', 'Orient'),
        ('Other', 'Other'),
    )
    
    name = models.CharField(max_length=300)
    brand = models.CharField(max_length=100, choices=BRAND_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.CharField(
        max_length=20,
        choices=[
            ('available', 'Available'),
            ('sold_out', 'Sold Out'),
            ('discontinued', 'Discontinued'),
        ],
        default='available'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_discount_percentage(self):
        if self.discount_price and self.discount_price < self.price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return int(discount)
        return 0


class CartItem(models.Model):
    """Mục trong giỏ hàng"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Order(models.Model):
    """Đơn hàng"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_address = models.TextField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    """Chi tiết đơn hàng"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.order.id} - {self.product.name}"
