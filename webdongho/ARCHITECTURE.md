# 🏗️ Kiến Trúc WatchShop - Sơ Đồ Hệ Thống

## 📊 Sơ Đồ Luồng Dữ Liệu

```
┌─────────────────────────────────────────────────────────────────┐
│                    NGƯỜI DÙNG (User)                              │
├─────────────────────────────────────────────────────────────────┤
│  - Username/Email                                                 │
│  - Password (Hashed)                                              │
│  - Orders (FK → Order)                                            │
│  - CartItems (FK → CartItem)                                      │
└─────────────────────────────────────────────────────────────────┘
         │                                              │
         │ (đăng ký/đăng nhập)          (thêm vào giỏ) │
         ▼                                              ▼
    ┌──────────────┐                          ┌─────────────────┐
    │  AUTH VIEW   │                          │  CART ITEM      │
    │ (login/reg)  │                          ├─────────────────┤
    └──────────────┘                          │ - User (FK)     │
                                              │ - Product (FK)  │
                                              │ - Quantity      │
                                              │ - Added_at      │
                                              └─────────────────┘
                                                     │
         ┌────────────────────────────────────────┬─┘
         │                                        │
         ▼                                        ▼
    ┌──────────────────┐              ┌──────────────────┐
    │   PRODUCT        │              │    ORDER         │
    ├──────────────────┤              ├──────────────────┤
    │ - Name           │              │ - User (FK)      │
    │ - Brand          │              │ - Total Amount   │
    │ - Category (FK)  │◄─────────────│ - Status         │
    │ - Price          │              │ - Delivery Addr  │
    │ - Discount Price │              │ - Phone Number   │
    │ - Image          │              │ - Created_at     │
    │ - Stock          │              └──────────────────┘
    │ - Status         │                      │
    └──────────────────┘                      │
         │                                   │ (thông qua)
         │                                   ▼
         │                            ┌──────────────────┐
         │                            │  ORDER ITEM      │
         │                            ├──────────────────┤
         └───────────────────────────►│ - Order (FK)     │
                                      │ - Product (FK)   │
                                      │ - Quantity       │
                                      │ - Price          │
                                      └──────────────────┘
         │
         │
         ▼
    ┌──────────────────┐
    │  CATEGORY        │
    ├──────────────────┤
    │ - Name           │
    │ - Description    │
    │ - Created_at     │
    └──────────────────┘
```

---

## 🔄 Quy Trình Mua Sắm

```
START
  │
  ├─► [TRANG CHỦ] - Xem sản phẩm nổi bật
  │     │
  │     └─► [DANH SÁCH SP] - Tìm kiếm, lọc
  │           │
  │           └─► [CHI TIẾT SP] - Xem thông tin
  │                 │
  │                 ├─► [ĐĂNG NHẬP/ĐĂNG KÝ] (Nếu chưa login)
  │                 │     │
  │                 │     └─► [FORM AUTH] 
  │                 │           │
  │                 │           └─► ✓ Tạo/Kiểm tra User
  │                 │
  │                 └─► [THÊM VÀO GIỎ]
  │                       │
  │                       └─► ✓ Tạo CartItem
  │
  ├─► [GIỎ HÀNG] - Xem, xóa sản phẩm
  │     │
  │     └─► [THANH TOÁN] - Nhập địa chỉ
  │           │
  │           ├─► ✓ Validate thông tin
  │           │
  │           └─► ✓ Tạo Order + OrderItems
  │                 │
  │                 ├─► ✓ Xóa CartItems
  │                 │
  │                 └─► ✓ Redirect đến Order Detail
  │
  ├─► [CHI TIẾT ĐƠN HÀNG] - Xem đơn
  │     │
  │     └─► [DANH SÁCH ĐƠN] - Tất cả đơn hàng
  │           │
  │           └─► [DASHBOARD] - Thống kê
  │
  └─► [ĐĂNG XUẤT]
        │
        └─► Session Cleared
             END
```

---

## 📁 URL Routing Structure

```
┌─ http://127.0.0.1:8000/
│
├─ / (home)
│  └─► shop.views.home
│
├─ /products/ (product_list)
│  └─► shop.views.product_list
│
├─ /product/<id>/ (product_detail)
│  └─► shop.views.product_detail
│
├─ /register/ (register)
│  └─► shop.views.register
│
├─ /login/ (login)
│  └─► shop.views.login_view
│
├─ /logout/ (logout) ⚠️ LOGIN REQUIRED
│  └─► shop.views.logout_view
│
├─ /cart/ (cart) ⚠️ LOGIN REQUIRED
│  └─► shop.views.cart
│
├─ /add-to-cart/ (add_to_cart) ⚠️ LOGIN REQUIRED, POST
│  └─► shop.views.add_to_cart
│
├─ /remove-from-cart/<id>/ ⚠️ LOGIN REQUIRED, POST
│  └─► shop.views.remove_from_cart
│
├─ /checkout/ (checkout) ⚠️ LOGIN REQUIRED
│  └─► shop.views.checkout
│
├─ /orders/ (order_list) ⚠️ LOGIN REQUIRED
│  └─► shop.views.order_list
│
├─ /order/<id>/ (order_detail) ⚠️ LOGIN REQUIRED
│  └─► shop.views.order_detail
│
├─ /dashboard/ (dashboard) ⚠️ LOGIN REQUIRED
│  └─► shop.views.dashboard
│
└─ /admin/
   └─► Django Admin Panel
```

---

## 🗂️ Template Inheritance Tree

```
base.html (Layout chính)
├─ HTML structure
├─ CSS styles
├─ Navigation
├─ Header
├─ Footer
└─ {% block content %}
   │
   ├─ home.html (Trang chủ)
   ├─ product_list.html (Danh sách SP)
   ├─ product_detail.html (Chi tiết SP)
   ├─ login.html (Đăng nhập)
   ├─ register.html (Đăng ký)
   ├─ cart.html (Giỏ hàng)
   ├─ checkout.html (Thanh toán)
   ├─ order_list.html (Danh sách đơn)
   ├─ order_detail.html (Chi tiết đơn)
   └─ dashboard.html (Dashboard)
```

---

## 🎯 Models Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                     DATABASE MODELS                          │
└─────────────────────────────────────────────────────────────┘

Category (1)
    │
    │ (1 to Many)
    │
    ▼
Product (Many)
    │
    ├─ (1 to Many) ─► CartItem (Many)
    │
    ├─ (1 to Many) ─► OrderItem (Many)
    │                   │
    │                   └─ (Many to 1) ─► Order (1)
    │
    └─ (FK) ──────────► Category

User (From Django)
    │
    ├─ (1 to Many) ─► CartItem (Many)
    │
    ├─ (1 to Many) ─► Order (Many)
    │                   │
    │                   └─ ManyToMany ─► Product
    │                      (thông qua OrderItem)
    │
    └─ (1 to Many) ─► Order (Many)

Order
    │
    ├─ (1 to Many) ─► OrderItem (Many)
    │                   │
    │                   └─ (Many to 1) ─► Product
    │
    └─ (Many to 1) ─► User
```

---

## 🔐 Authentication Flow

```
┌─ User accesses protected page
│
├─► Is user logged in?
│   │
│   ├─ NO ─► Redirect to /login/
│   │         │
│   │         └─ User enters credentials
│   │           │
│   │           ├─► Django checks against DB
│   │           │
│   │           ├─► Valid ✓
│   │           │   │
│   │           │   └─► Create session
│   │           │       │
│   │           │       └─► Redirect to requested page
│   │           │
│   │           └─► Invalid ✗
│   │               │
│   │               └─► Show error message
│   │                   Retry login
│   │
│   └─ YES ✓
│       │
│       └─► Grant access to page
│           │
│           └─► User can access all protected features
│               (cart, checkout, orders, dashboard)
│
└─► User logout
    │
    └─► Session cleared
        Session cookie deleted
        Redirect to home
```

---

## 💾 Data Flow in Checkout

```
[Giỏ Hàng] 
    │
    └─► CartItem records in DB
        │
        └─► User submits Checkout Form
            │
            ├─► Validate Address & Phone
            │
            └─► Calculate Total Amount
                │
                ├─► Create Order
                │   │
                │   ├─ Order.user = current_user
                │   ├─ Order.total_amount = sum(prices)
                │   ├─ Order.delivery_address = form data
                │   ├─ Order.phone_number = form data
                │   └─ Order.status = 'pending'
                │
                └─► For each CartItem:
                    │
                    ├─► Create OrderItem
                    │   │
                    │   ├─ OrderItem.order = new order
                    │   ├─ OrderItem.product = cartitem.product
                    │   ├─ OrderItem.quantity = cartitem.quantity
                    │   └─ OrderItem.price = product.discount_price or price
                    │
                    └─► Delete CartItem
                        │
                        └─► Success!
                            │
                            └─► Redirect to Order Detail
```

---

## 🎨 CSS Architecture

```
CSS in base.html
│
├─ :root (CSS Variables)
│  ├─ --primary: #2c3e50 (Xanh đậm)
│  ├─ --secondary: #e74c3c (Đỏ)
│  ├─ --light: #ecf0f1 (Xám sáng)
│  ├─ --dark: #1a1a1a (Đen)
│  └─ --success: #27ae60 (Xanh lá)
│
├─ Global Styles
│  ├─ * (Reset)
│  └─ body, html
│
├─ Layout Components
│  ├─ header (sticky)
│  ├─ nav (responsive)
│  ├─ main
│  ├─ footer
│  └─ container (max-width: 1200px)
│
├─ Utility Classes
│  ├─ .btn (Button)
│  ├─ .form-group (Form)
│  ├─ .alert (Messages)
│  └─ Spacing (mb-*, mt-*, etc.)
│
├─ Component Styles
│  ├─ .product-grid (CSS Grid)
│  ├─ .product-card (Flex)
│  ├─ table (Striped)
│  └─ form elements
│
└─ Responsive Media Queries
   └─ @media (max-width: 768px)
```

---

## 🚀 Deployment Ready Features

- ✅ Static files configured
- ✅ Settings production-ready
- ✅ CSRF protection enabled
- ✅ Password hashing secure
- ✅ Database migrations automatic
- ✅ Admin panel secured
- ✅ Error handling implemented
- ✅ Message framework integrated

---

## 📈 Performance Considerations

- ✅ QuerySet optimization (select_related, prefetch_related)
- ✅ Template caching possible
- ✅ Static file serving ready
- ✅ Database indexing possible
- ✅ Pagination ready to implement
- ✅ Lazy loading possible

---

## 🔮 Future Enhancements

```
├─ Payment Gateway Integration
│  ├─ Stripe API
│  ├─ PayPal API
│  └─ VNPay (Vietnam specific)
│
├─ Email Notifications
│  ├─ Order confirmation
│  ├─ Shipping updates
│  └─ Review reminders
│
├─ User Features
│  ├─ Profile management
│  ├─ Wishlist
│  ├─ Reviews & Ratings
│  └─ Address book
│
├─ Admin Features
│  ├─ Advanced analytics
│  ├─ Inventory management
│  ├─ Sales reports
│  └─ Customer management
│
├─ Search & Filter
│  ├─ Full-text search
│  ├─ Advanced filters
│  ├─ Sort options
│  └─ Saved searches
│
└─ Social
   ├─ Social login
   ├─ Share to social
   ├─ Reviews with images
   └─ Referral program
```

---

## 📞 Technical Support

Để hiểu rõ hơn các phần của kiến trúc:
- Xem `README.md` - Tài liệu chi tiết
- Xem `models.py` - Cấu trúc dữ liệu
- Xem `views.py` - Xử lý business logic
- Xem `urls.py` - Định tuyến đầu vào
- Xem `templates/base.html` - Giao diện chính

---

**Kiến trúc này được thiết kế để dễ mở rộng và bảo trì! 🏗️**
