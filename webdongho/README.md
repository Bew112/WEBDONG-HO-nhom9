# 🕐 WatchShop - Website Bán Đồng Hồ Chính Hãng

Một ứng dụng web e-commerce hiện đại được xây dựng bằng Django, chuyên về bán các loại đồng hồ chính hãng từ các thương hiệu hàng đầu thế giới như Rolex, Omega, TAG Heuer, Patek Philippe, và nhiều thương hiệu khác.

---

## 📋 Mục Lục
- [Tính Năng Chính](#tính-năng-chính)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Hướng Dẫn Chạy](#hướng-dẫn-chạy)
- [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
- [Cơ Sở Dữ Liệu](#cơ-sở-dữ-liệu)
- [Tài Liệu API](#tài-liệu-api)
- [Ghi Chú Phát Triển](#ghi-chú-phát-triển)

---

## ✨ Tính Năng Chính

### 1. **Quản Lý Sản Phẩm**
- ✅ Hiển thị danh sách sản phẩm với chi tiết đầy đủ
- ✅ Tìm kiếm sản phẩm theo tên, thương hiệu
- ✅ Lọc sản phẩm theo danh mục (Luxury, Sports, Casual, Dress)
- ✅ Lọc theo khoảng giá
- ✅ Hiển thị sản phẩm nổi bật trên trang chủ
- ✅ Thông tin chi tiết sản phẩm liên quan

### 2. **Hệ Thống Xác Thực Người Dùng**
- ✅ Đăng ký tài khoản mới
- ✅ Đăng nhập an toàn
- ✅ Đăng xuất
- ✅ Quản lý hồ sơ người dùng
- ✅ Xác thực quyền truy cập

### 3. **Giỏ Hàng & Thanh Toán**
- ✅ Thêm/xóa sản phẩm vào giỏ hàng
- ✅ Cập nhật số lượng sản phẩm
- ✅ Tính toán tổng giá trị giỏ hàng
- ✅ Giao diện checkout thân thiện
- ✅ Nhập thông tin giao hàng
- ✅ Thanh toán khi nhận hàng (COD)

### 4. **Quản Lý Đơn Hàng**
- ✅ Tạo đơn hàng từ giỏ hàng
- ✅ Xem danh sách đơn hàng của người dùng
- ✅ Xem chi tiết từng đơn hàng
- ✅ Theo dõi trạng thái đơn hàng (Chờ duyệt, Đã duyệt, Từ chối)
- ✅ Lưu trữ thông tin giao hàng

### 5. **Dashboard Cá Nhân**
- ✅ Hiển thị thống kê: số đơn hàng, tổng chi tiêu
- ✅ Thông tin tài khoản người dùng
- ✅ Liên kết nhanh đến các chức năng chính

### 6. **Giao Diện Người Dùng**
- ✅ Responsive Design (Desktop, Tablet, Mobile)
- ✅ Navigation bar với các liên kết chính
- ✅ Footer với thông tin liên hệ
- ✅ Layout chung (base template inheritance)
- ✅ Thông báo (messages) đẹp và rõ ràng

### 7. **Quản Trị Viên**
- ✅ Admin panel toàn diện
- ✅ Quản lý sản phẩm, danh mục, đơn hàng
- ✅ Dữ liệu demo (seed data)

---

## 🔧 Yêu Cầu Hệ Thống

- **Python:** 3.9+
- **Django:** 6.0.1+
- **Database:** SQLite3 (mặc định), hoặc MySQL, PostgreSQL
- **Trình duyệt:** Chrome, Firefox, Safari, Edge (phiên bản mới nhất)

---

## 📦 Cài Đặt

### Bước 1: Clone hoặc tải dự án
```bash
cd d:\Python\ web\webdongho
```

### Bước 2: Tạo Virtual Environment
```bash
python -m venv venv
```

### Bước 3: Kích hoạt Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Bước 4: Cài đặt Dependencies
```bash
pip install django==6.0.1
```

Hoặc nếu có requirements.txt:
```bash
pip install -r requirements.txt
```

### Bước 5: Chạy Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Bước 6: Load Seed Data
```bash
python manage.py seed_data
```

### Bước 7: Tạo Tài Khoản Admin
```bash
python manage.py createsuperuser
```

---

## 🚀 Hướng Dẫn Chạy

### Khởi Động Server Phát Triển
```bash
python manage.py runserver
```

Server sẽ chạy tại: `http://127.0.0.1:8000/`

### Truy Cập Admin Panel
```
http://127.0.0.1:8000/admin/
```

Đăng nhập bằng tài khoản admin đã tạo.

### Tài Khoản Demo (Sau khi load seed data)
- Bạn có thể tạo tài khoản mới qua trang `/register/`
- Hoặc sử dụng admin panel để quản lý người dùng

---

## 📁 Cấu Trúc Dự Án

```
webdongho/
├── manage.py                      # Django management script
├── db.sqlite3                     # Database (SQLite)
│
├── webdongho/                     # Project configuration
│   ├── __init__.py
│   ├── settings.py                # Cài đặt chính
│   ├── urls.py                    # URL routing chính
│   ├── asgi.py                    # ASGI config
│   └── wsgi.py                    # WSGI config
│
├── shop/                          # Ứng dụng chính
│   ├── migrations/                # Database migrations
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py       # Load dữ liệu demo
│   ├── __init__.py
│   ├── admin.py                   # Admin configuration
│   ├── apps.py
│   ├── models.py                  # Database models
│   ├── views.py                   # Views
│   ├── urls.py                    # URL routing
│   └── tests.py
│
└── templates/                     # HTML templates
    └── shop/
        ├── base.html              # Template chung
        ├── home.html              # Trang chủ
        ├── product_list.html      # Danh sách sản phẩm
        ├── product_detail.html    # Chi tiết sản phẩm
        ├── login.html             # Trang đăng nhập
        ├── register.html          # Trang đăng ký
        ├── cart.html              # Giỏ hàng
        ├── checkout.html          # Thanh toán
        ├── order_list.html        # Danh sách đơn hàng
        ├── order_detail.html      # Chi tiết đơn hàng
        └── dashboard.html         # Dashboard cá nhân
```

---

## 🗄️ Cơ Sở Dữ Liệu

### Models (Mô Hình Dữ Liệu)

#### 1. **Category** - Danh Mục Sản Phẩm
```python
- id (PrimaryKey)
- name (CharField, max_length=200, unique)
- description (TextField)
- created_at (DateTimeField)
```

#### 2. **Product** - Sản Phẩm Đồng Hồ
```python
- id (PrimaryKey)
- name (CharField)
- brand (CharField, choices)
- category (ForeignKey → Category)
- description (TextField)
- price (DecimalField)
- discount_price (DecimalField, nullable)
- image (URLField)
- stock (IntegerField)
- status (CharField: available/sold_out/discontinued)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

#### 3. **CartItem** - Mục Giỏ Hàng
```python
- id (PrimaryKey)
- user (ForeignKey → User)
- product (ForeignKey → Product)
- quantity (IntegerField)
- added_at (DateTimeField)
```

#### 4. **Order** - Đơn Hàng
```python
- id (PrimaryKey)
- user (ForeignKey → User)
- total_amount (DecimalField)
- status (CharField: pending/approved/rejected)
- delivery_address (TextField)
- phone_number (CharField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

#### 5. **OrderItem** - Chi Tiết Đơn Hàng
```python
- id (PrimaryKey)
- order (ForeignKey → Order)
- product (ForeignKey → Product)
- quantity (IntegerField)
- price (DecimalField)
```

---

## 📚 Tài Liệu API / URLs

### Public URLs
| URL | Phương Thức | Mô Tả |
|-----|----------|------|
| `/` | GET | Trang chủ |
| `/products/` | GET | Danh sách sản phẩm |
| `/product/<id>/` | GET | Chi tiết sản phẩm |
| `/register/` | GET, POST | Đăng ký tài khoản |
| `/login/` | GET, POST | Đăng nhập |

### Protected URLs (Cần đăng nhập)
| URL | Phương Thức | Mô Tả |
|-----|----------|------|
| `/logout/` | GET | Đăng xuất |
| `/cart/` | GET | Xem giỏ hàng |
| `/add-to-cart/` | POST | Thêm vào giỏ hàng |
| `/remove-from-cart/<id>/` | POST | Xóa khỏi giỏ hàng |
| `/checkout/` | GET, POST | Thanh toán |
| `/orders/` | GET | Danh sách đơn hàng |
| `/order/<id>/` | GET | Chi tiết đơn hàng |
| `/dashboard/` | GET | Dashboard cá nhân |

---

## 📝 Ghi Chú Phát Triển

### Các Thương Hiệu Đồng Hồ
- Rolex
- Omega
- Cartier
- TAG Heuer
- Patek Philippe
- IWC
- Seiko
- Casio
- Orient

### Danh Mục Sản Phẩm
1. **Luxury** - Đồng hồ hạng sang
2. **Sports** - Đồng hồ thể thao
3. **Casual** - Đồng hồ casual hàng ngày
4. **Dress** - Đồng hồ lịch sự

### Trạng Thái Sản Phẩm
- `available` - Có sẵn
- `sold_out` - Hết hàng
- `discontinued` - Ngừng kinh doanh

### Trạng Thái Đơn Hàng
- `pending` - Chờ duyệt
- `approved` - Đã duyệt
- `rejected` - Từ chối

---

## 🎨 Giao Diện & Styling

### Màu Sắc Chính
- **Primary:** `#2c3e50` (Xanh đậm)
- **Secondary:** `#e74c3c` (Đỏ)
- **Success:** `#27ae60` (Xanh lá)
- **Light:** `#ecf0f1` (Xám sáng)
- **Dark:** `#1a1a1a` (Đen)

### Responsive Breakpoints
- Desktop: > 1024px
- Tablet: 768px - 1024px
- Mobile: < 768px

---

## 🐛 Troubleshooting

### Migration Errors
```bash
# Xóa migrations
rm db.sqlite3
rm shop/migrations/0*.py

# Tạo lại
python manage.py makemigrations shop
python manage.py migrate
```

### Port 8000 đã được sử dụng
```bash
python manage.py runserver 8080
```

### Import Errors
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📞 Hỗ Trợ & Liên Hệ

- **Email:** support@watchshop.vn
- **Hotline:** 1900-XXXX
- **GitHub:** [Link repository]

---

## 📄 License

Project này được phát triển cho mục đích học tập và thương mại. Mọi quyền lợi được bảo vệ.

---

## ✅ Checklist Hoàn Thành

- [x] 1. Dự án tạo thành công bằng Django/Flask
- [x] 2. Thiết kế giao diện chính (Home, Login, Dashboard, CRUD)
- [x] 3. Giao diện có bộ cục hợp lý, responsive
- [x] 4. Kết nối thành công với CSDL (SQLite)
- [x] 5. Tạo được ít nhất 2 bảng dữ liệu chính (Product, Category, Order, CartItem, OrderItem)
- [x] 6. Hiển thị dữ liệu mẫu (seed data) trên trang web
- [x] 7. Cài đặt đăng nhập - đăng ký cơ bản hoạt động
- [x] 8. Có menu điều hướng, header, footer thông nhất
- [x] 9. Triển khai template inheritance (layout chung)
- [x] 10. Cập nhật README.md với mô tả & hướng dẫn chạy thử

---

**Được phát triển bởi:** Chuyên gia lập trình viên Django  
**Ngày tạo:** Tháng 1 năm 2026  
**Phiên bản:** 1.0.0
