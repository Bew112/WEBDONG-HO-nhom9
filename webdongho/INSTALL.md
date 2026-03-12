# 📖 Hướng Dẫn Cài Đặt Chi Tiết - WatchShop

## 💻 Yêu Cầu Hệ Thống

- **OS:** Windows 10/11, macOS, Linux
- **Python:** 3.9 hoặc cao hơn
- **RAM:** Tối thiểu 2GB
- **Ổ cứng:** 500MB trống

---

## 🔧 Hướng Dẫn Cài Đặt Từng Bước

### Bước 1: Cài Python

1. Tải Python từ: https://www.python.org/downloads/
2. Tại thời điểm cài đặt, **✓ Check "Add Python to PATH"**
3. Nhấn "Install Now"

**Kiểm tra cài đặt:**
```bash
python --version
```

---

### Bước 2: Mở Terminal/Command Prompt

**Windows:**
- Nhấn `Win + R`, gõ `cmd`, nhấn Enter

**macOS/Linux:**
- Mở Terminal

---

### Bước 3: Chuyển Vào Thư Mục Dự Án

```bash
cd d:\Python\ web\webdongho
```

*Lưu ý: Thay đổi đường dẫn nếu bạn lưu dự án ở chỗ khác*

---

### Bước 4: Tạo Virtual Environment

```bash
python -m venv venv
```

**Lý do:** Virtual environment giúp cô lập các thư viện Python của dự án này

---

### Bước 5: Kích Hoạt Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

*Sau khi kích hoạt, bạn sẽ thấy `(venv)` ở đầu dòng terminal*

---

### Bước 6: Cài Đặt Django

```bash
pip install -r requirements.txt
```

**Hoặc cài riêng lẻ:**
```bash
pip install Django==6.0.1
```

---

### Bước 7: Chạy Migrations (Tạo Database)

```bash
python manage.py migrate
```

Lệnh này sẽ tạo file `db.sqlite3` chứa cơ sở dữ liệu

---

### Bước 8: Tải Dữ Liệu Mẫu

```bash
python manage.py seed_data
```

Lệnh này sẽ tạo:
- ✓ 4 danh mục sản phẩm
- ✓ 10 sản phẩm đồng hồ mẫu

---

### Bước 9: Khởi Động Server

```bash
python manage.py runserver
```

**Output sẽ như thế này:**
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
January 28, 2026 - 21:34:12
Django version 6.0.1, using settings 'webdongho.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### Bước 10: Truy Cập Website

Mở trình duyệt (Chrome, Firefox, Safari, Edge) và truy cập:

```
http://127.0.0.1:8000/
```

---

## 🎯 Các URL Chính

| URL | Mô Tả |
|-----|-------|
| `http://127.0.0.1:8000/` | Trang chủ |
| `http://127.0.0.1:8000/products/` | Danh sách sản phẩm |
| `http://127.0.0.1:8000/register/` | Đăng ký tài khoản |
| `http://127.0.0.1:8000/login/` | Đăng nhập |
| `http://127.0.0.1:8000/admin/` | Admin panel |

---

## 🔐 Tạo Tài Khoản Admin

```bash
python manage.py createsuperuser
```

**Nhập thông tin:**
```
Username: admin
Email: admin@example.com
Password: (gõ mật khẩu)
Password (again): (xác nhận)
```

**Sau đó đăng nhập tại:** `http://127.0.0.1:8000/admin/`

---

## 🧪 Kiểm Tra Cài Đặt

### Check 1: Kiểm tra Django
```bash
python -m django --version
```
Nên hiển thị: `6.0.1`

### Check 2: Kiểm tra Database
```bash
python manage.py dbshell
```
Nếu thành công, nó sẽ mở database shell

### Check 3: Kiểm tra Models
```bash
python manage.py shell
>>> from shop.models import Product
>>> Product.objects.all().count()
```
Nên hiển thị: `10`

---

## 🛑 Dừng Server

Nhấn `Ctrl + C` trong terminal (Windows: `Ctrl + Break`)

---

## 📚 Các Lệnh Hữu Ích

### Tạo Migration (khi thay đổi models)
```bash
python manage.py makemigrations
```

### Áp dụng Migration
```bash
python manage.py migrate
```

### Mở Django Shell (Python REPL)
```bash
python manage.py shell
```

### Tạo superuser mới
```bash
python manage.py createsuperuser
```

### Xóa tất cả dữ liệu (cẩn thận!)
```bash
python manage.py flush
```

### Chạy tests
```bash
python manage.py test
```

---

## 🐛 Lỗi Thường Gặp & Cách Giải Quyết

### ❌ Error: "Python is not recognized"

**Giải pháp:**
1. Kiểm tra Python đã cài chưa: `python --version`
2. Thêm Python vào PATH
3. Khởi động lại terminal

---

### ❌ Error: "ModuleNotFoundError: No module named 'django'"

**Giải pháp:**
```bash
pip install Django==6.0.1
```

---

### ❌ Error: "Port 8000 already in use"

**Giải pháp:**
```bash
# Chạy trên port khác
python manage.py runserver 8080

# Hoặc tìm process sử dụng port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### ❌ Error: "db.sqlite3 permission denied"

**Giải pháp:**
1. Tắt Visual Studio Code
2. Xóa file `db.sqlite3`
3. Chạy lại `python manage.py migrate`

---

### ❌ Error: "No module named 'webdongho.settings'"

**Giải pháp:**
1. Kiểm tra đang ở thư mục đúng: `cd d:\Python\ web\webdongho`
2. Check file `manage.py` tồn tại
3. Kiểm tra virtual environment kích hoạt

---

## 🔄 Khôi Phục Từ Đầu

Nếu mọi thứ không hoạt động, hãy thử:

```bash
# 1. Xóa database
del db.sqlite3

# 2. Xóa pycache (Windows)
del /s __pycache__

# 3. Tạo lại từ đầu
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

---

## 📞 Cần Trợ Giúp?

1. **Đọc README.md** - Có thông tin chi tiết hơn
2. **Xem Django Docs** - https://docs.djangoproject.com/
3. **Liên hệ:** support@watchshop.vn

---

## ✅ Bảng Kiểm Tra Sau Cài Đặt

- [ ] Python 3.9+ đã cài
- [ ] Virtual environment hoạt động
- [ ] Django 6.0.1 đã cài
- [ ] Database migrations đã chạy
- [ ] Seed data đã tải
- [ ] Server khởi động thành công
- [ ] Có thể truy cập http://127.0.0.1:8000/
- [ ] Có 10 sản phẩm trong cơ sở dữ liệu

---

**Chúc mừng! Website của bạn đã sẵn sàng! 🎉**
