# 🚀 Hướng Dẫn Nhanh - WatchShop

## Bắt Đầu Nhanh (2 phút)

### 1. Cài Đặt & Chạy

```bash
# Chuyển vào thư mục
cd d:\Python\ web\webdongho

# Tạo virtual environment
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Cài dependencies
pip install -r requirements.txt

# Chạy migrations
python manage.py migrate

# Load dữ liệu mẫu
python manage.py seed_data

# Khởi động server
python manage.py runserver
```

### 2. Truy Cập Website

- **Trang chủ:** http://127.0.0.1:8000/
- **Cửa hàng:** http://127.0.0.1:8000/products/
- **Admin:** http://127.0.0.1:8000/admin/

### 3. Tạo Tài Khoản Admin (tuỳ chọn)

```bash
python manage.py createsuperuser
```

---

## 🎯 Tính Năng Chính

✅ **Trang Chủ** - Hiển thị sản phẩm nổi bật  
✅ **Cửa Hàng** - Duyệt, tìm kiếm, lọc sản phẩm  
✅ **Chi Tiết Sản Phẩm** - Xem thông tin đầy đủ  
✅ **Đăng Ký/Đăng Nhập** - Quản lý tài khoản  
✅ **Giỏ Hàng** - Thêm/xóa sản phẩm  
✅ **Thanh Toán** - Nhập thông tin giao hàng  
✅ **Đơn Hàng** - Theo dõi đơn hàng  
✅ **Dashboard** - Thống kê cá nhân  

---

## 📊 Dữ Liệu Mẫu (Seed Data)

Có **10 sản phẩm** từ các thương hiệu nổi tiếng:
- 🏆 Rolex, Omega, Patek Philippe (Hạng sang)
- ⚽ TAG Heuer, Seiko, Casio (Thể thao)
- 👔 Cartier, IWC (Lịch sự)
- 😎 Orient, Timex (Casual)

---

## 🔑 Tài Khoản Demo

Tạo tài khoản mới tại: `/register/`

Hoặc sử dụng:
- **Username:** admin
- **Password:** (tạo khi chạy `createsuperuser`)

---

## 📁 Cấu Trúc Thư Mục

```
webdongho/
├── shop/                 # Ứng dụng chính
│   ├── models.py        # Cơ sở dữ liệu
│   ├── views.py         # Xử lý logic
│   ├── urls.py          # Định tuyến
│   └── admin.py         # Admin panel
├── templates/           # Giao diện HTML
├── manage.py           # Django tool
└── requirements.txt    # Thư viện cần thiết
```

---

## ⚠️ Lỗi Thường Gặp

**Port 8000 đã dùng?**
```bash
python manage.py runserver 8080
```

**Database lỗi?**
```bash
python manage.py migrate --run-syncdb
```

**Import error?**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📞 Hỗ Trợ

- Xem chi tiết: `README.md`
- Email: support@watchshop.vn

---

**Happy Shopping! 🛍️**
