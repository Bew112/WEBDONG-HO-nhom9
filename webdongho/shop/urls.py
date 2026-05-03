from django.urls import path 
from . import views



urlpatterns = [
    # Home & Product
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Cart & Order
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/', views.buy_now, name='buy_now'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/<int:pk>/qr/', views.order_payment_qr, name='order_payment_qr'),
    
    # Statistics & Reports
    path('statistics/', views.statistics_dashboard, name='statistics'),
    path('reports/revenue/', views.revenue_report, name='revenue_report'),
    path('reports/category/', views.category_report, name='category_report'),
    path('reports/products/', views.product_report, name='product_report'),
    path('reports/order-status/', views.order_status_report, name='order_status_report'),
]
