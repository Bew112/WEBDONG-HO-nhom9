# 📊 Thiết Kế Cơ Sở Dữ Liệu - Watch Shop

## 📋 Tổng Quan

Cơ sở dữ liệu được thiết kế với **7 bảng chính** có quan hệ chặt chẽ, đảm bảo tính toàn vẹn dữ liệu, tránh dữ liệu trùng lặp, và hỗ trợ các tính năng kinh doanh như quản lý sản phẩm, đơn hàng, đánh giá và vận chuyển.

---

## 🔑 Các Bảng Dữ Liệu

### 1️⃣ **Brand (Thương Hiệu)**

| Cột | Kiểu Dữ Liệu | Ràng Buộc | Mô Tả |
|-----|-------------|----------|--------|
| `id` (PK) | AutoField | PRIMARY KEY | Định danh duy nhất |
| `name` | CharField(100) | UNIQUE, NOT NULL | Tên thương hiệu (Rolex, Omega, ...) |
| `country` | CharField(50) | BLANK | Quốc gia sản xuất |
| `founded_year` | IntegerField | NULL, BLANK | Năm thành lập |
| `description` | TextField | BLANK | Mô tả chi tiết |
| `logo` | ImageField | NULL, BLANK | Logo thương hiệu |
| `created_at` | DateTimeField | AUTO_NOW_ADD | Thời gian tạo |

**Vai Trò:** Lưu trữ thông tin các thương hiệu đồng hồ. Tách riêng thành bảng để tránh dữ liệu trùng lặp và dễ quản lý.

---

### 2️⃣ **Category (Danh Mục)**

| Cột | Kiểu Dữ Liệu | Ràng Buộc | Mô Tả |
|-----|-------------|----------|--------|
| `id` (PK) | AutoField | PRIMARY KEY | Định danh duy nhất |
| `name` | CharField(200) | UNIQUE, NOT NULL | Tên danh mục (Casual, Dress, Luxury, ...) |
| `description` | TextField | BLANK | Mô tả danh mục |
| `created_at` | DateTimeField | AUTO_NOW_ADD | Thời gian tạo |

**Vai Trò:** Phân loại sản phẩm theo loại đồng hồ.

---

### 3️⃣ **Product (Sản Phẩm)**

| Cột | Kiểu Dữ Liệu | Ràng Buộc | Mô Tả |
|-----|-------------|----------|--------|
| `id` (PK) | AutoField | PRIMARY KEY | Định danh duy nhất |
| `name` | CharField(300) | NOT NULL | Tên sản phẩm |
| `brand_id` (FK) | ForeignKey(Brand) | NOT NULL, ON_DELETE=PROTECT | ⭐ Tham chiếu đến Brand |
| `category_id` (FK) | ForeignKey(Category) | NOT NULL, ON_DELETE=CASCADE | ⭐ Tham chiếu đến Category |
| `description` | TextField | NOT NULL | Mô tả chi tiết |
| `price` | DecimalField(12,2) | ≥ 0 | Giá gốc |
| `discount_price` | DecimalField(12,2) | < price, NULL | Giá sau chiết khấu |
| `image` | ImageField | BLANK, NULL | Ảnh sản phẩm |
| `stock` | IntegerField | ≥ 0 | Số lượng tồn kho |
| `status` | CharField | CHOICES | available, sold_out, discontinued, pre_order |
| `sku` | CharField(100) | UNIQUE, BLANK | Mã SKU |
| `warranty_months` | IntegerField | ≥ 1 | Thời gian bảo hành (tháng) |
| `created_at` | DateTimeField | AUTO_NOW_ADD | Thời gian tạo |
| `updated_at` | DateTimeField | AUTO_NOW | Thời gian cập nhật |

**Ràng Buộc Duy Nhất:** 
- `unique_brand_product_name`: Không có 2 sản phẩm cùng tên từ cùng 1 thương hiệu

**Vai Trò:** Lưu trữ thông tin chi tiết sản phẩm. Sử dụng `ON_DELETE=PROTECT` cho brand để tránh xóa thương hiệu nếu còn sản phẩm.

---

### 4️⃣ **ProductRating (Đánh Giá Sản Phẩm)**

| Cột | Kiểu Dữ Liệu | Ràng Buộc | Mô Tả |
|-----|-------------|----------|--------|
| `id` (PK) | AutoField | PRIMARY KEY | Định danh duy nhất |
| `product_id` (FK) | ForeignKey(Product) | NOT NULL, ON_DELETE=CASCADE | ⭐ Tham chiếu sản phẩm |
| `user_id` (FK) | ForeignKey(User) | NOT NULL, ON_DELETE=CASCADE | ⭐ Tham chiếu người dùng |
| `rating` | IntegerField | 1-5, NOT NULL | Điểm đánh giá (1-5 sao) |
| `comment` | TextField | BLANK | Bình luận |
| `created_at` | DateTimeField | AUTO_NOW_ADD | Thời gian tạo |
| `updated_at` | DateTimeField | AUTO_NOW | Thời gian cập nhật |

**Ràng Buộc Duy Nhất:**
- `unique_together: [product, user]`: Mỗi người chỉ đánh giá 1 lần cho 1 sản phẩm

**Vai Trò:** Lưu trữ đánh giá của khách hàng, hỗ trợ tính điểm trung bình sản phẩm.

---

### 5️⃣ **CartItem (Mục Giỏ Hàng)**

| Cột | Kiểu Dữ Liệu | Ràng Buộc | Mô Tả |
|-----|-------------|----------|--------|
| `id` (PK) | AutoField | PRIMARY KEY | Định danh duy nhất |
| `user_id` (FK) | ForeignKey(User) | NOT NULL, ON_DELETE=CASCADE | ⭐ Tham chiếu người dùng |
| `product_id` (FK) | ForeignKey(Product) | NOT NULL, ON_DELETE=CASCADE | ⭐ Tham chiếu sản phẩm |
| `quantity` | IntegerField | ≥ 1 | Số lượng |
| `added_at` | DateTimeField | AUTO_NOW_ADD | Thời gian thêm |
| `updated_at` | DateTimeField | AUTO_NOW | Thời gian cập nhật |

**Ràng Buộc Duy Nhất:**
- `unique_together: [user, product]`: Không có 2 item giống nhau trong giỏ

**Vai Trò:** Lưu trữ giỏ hàng của khách hàng.

---

### 6️⃣ **Order (Đơn Hàng)**

| Cột | Kiểu Dữ Liệu | Ràng Buộc | Mô Tả |
|-----|-------------|----------|--------|
| `id` (PK) | AutoField | PRIMARY KEY | Định danh duy nhất |
| `user_id` (FK) | ForeignKey(User) | NOT NULL, ON_DELETE=CASCADE | ⭐ Khách hàng đặt hàng |
| `total_amount` | DecimalField(12,2) | ≥ 0 | Tổng tiền |
| `status` | CharField | CHOICES | pending, confirmed, shipping, delivered, cancelled, returned |
| `delivery_address` | TextField | NOT NULL | Địa chỉ giao hàng |
| `phone_number` | CharField(20) | NOT NULL | Số điện thoại |
| `email` | EmailField | BLANK, NULL | Email |
| `notes` | TextField | BLANK | Ghi chú từ khách |
| `created_at` | DateTimeField | AUTO_NOW_ADD | Thời gian tạo |
| `updated_at` | DateTimeField | AUTO_NOW | Thời gian cập nhật |

**Vai Trò:** Lưu trữ thông tin đơn hàng từ khách hàng.

---

### 7️⃣ **OrderItem (Chi Tiết Đơn Hàng)**

| Cột | Kiểu Dữ Liệu | Ràng Buộc | Mô Tả |
|-----|-------------|----------|--------|
| `id` (PK) | AutoField | PRIMARY KEY | Định danh duy nhất |
| `order_id` (FK) | ForeignKey(Order) | NOT NULL, ON_DELETE=CASCADE | ⭐ Đơn hàng cha |
| `product_id` (FK) | ForeignKey(Product) | NOT NULL, ON_DELETE=PROTECT | ⭐ Sản phẩm (bảo vệ xóa) |
| `quantity` | IntegerField | ≥ 1 | Số lượng đã mua |
| `price` | DecimalField(12,2) | ≥ 0 | Giá bán (lúc đặt) |

**Ràng Buộc Duy Nhất:**
- `unique_together: [order, product]`: Không lặp lại sản phẩm trong 1 đơn hàng

**Vai Trò:** Lưu trữ chi tiết từng sản phẩm trong đơn hàng, giá được ghi lại để tránh ảnh hưởng khi thay đổi giá sản phẩm.

---

### 8️⃣ **Shipment (Vận Chuyển)**

| Cột | Kiểu Dữ Liệu | Ràng Buộc | Mô Tả |
|-----|-------------|----------|--------|
| `id` (PK) | AutoField | PRIMARY KEY | Định danh duy nhất |
| `order_id` (FK) | OneToOneField(Order) | NOT NULL, ON_DELETE=CASCADE | ⭐ Đơn hàng (1:1) |
| `carrier` | CharField(100) | NOT NULL | Hãng vận chuyển (ViettelPost, GHN, ...) |
| `tracking_number` | CharField(100) | UNIQUE, NOT NULL | Mã tracking |
| `status` | CharField | CHOICES | pending, picked_up, in_transit, out_for_delivery, delivered, failed |
| `estimated_delivery` | DateTimeField | NULL | Ngày dự kiến giao |
| `actual_delivery` | DateTimeField | NULL | Ngày thực tế giao |
| `created_at` | DateTimeField | AUTO_NOW_ADD | Thời gian tạo |
| `updated_at` | DateTimeField | AUTO_NOW | Cập nhật |

**Vai Trò:** Theo dõi vận chuyển đơn hàng, hỗ trợ kiểm tra tình trạng giao hàng.

---

## 📌 Sơ Đồ Quan Hệ (ERD)

```
┌─────────────┐
│   User      │ (Django built-in)
│ (pk) id     │
└──────┬──────┘
       │ (1)
       │
       ├─ has many →  CartItem
       │  (user_id FK)
       │
       ├─ has many →  Order
       │  (user_id FK)
       │
       └─ has many →  ProductRating
          (user_id FK)

┌─────────────┐         ┌─────────────┐
│   Brand     │ ←─────→ │   Product   │
│ (pk) id     │ (1)  (M)│ (pk) id     │
│ name        │         │ name        │
│ country     │         │ brand_id FK │
└─────────────┘         │ category_id │
                        │ price       │
                        │ discount_pr │
                        │ stock       │
                        │ status      │
                        │ warranty    │
                        └──────┬──────┘
                               │ (1)
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                │ (M)          │ (M)          │ (M)
                │              │              │
          CartItem       ProductRating    OrderItem
        (product_id)    (product_id)    (product_id)
             │              │              │
             │              │              │
             └──────────────┤──────────────┘
                            │
                     ┌──────┴──────┐
                     │             │
                ┌────▼────┐   ┌────▼────┐
                │  Order  │   │ Shipment │
                │ (pk) id │←──│(order_id)│
                │status   │   │tracking# │
                │total    │   │status    │
                │address  │   │carrier   │
                └─────────┘   └──────────┘


┌─────────────┐
│  Category   │
│ (pk) id     │
└──────┬──────┘
       │ (1)
       │
       └─ has many → Product
          (category_id FK)
```

---

## 🔄 Quan Hệ Chi Tiết

### **Foreign Key Relationships:**

| Quan Hệ | Từ Bảng | Đến Bảng | ON_DELETE | Mô Tả |
|---------|---------|---------|-----------|--------|
| Product → Brand | product.brand_id | brand.id | PROTECT | Không xóa brand nếu còn sản phẩm |
| Product → Category | product.category_id | category.id | CASCADE | Xóa category → xóa sản phẩm |
| CartItem → User | cartitem.user_id | user.id | CASCADE | Xóa user → xóa giỏ |
| CartItem → Product | cartitem.product_id | product.id | CASCADE | Xóa sản phẩm → xóa mục giỏ |
| ProductRating → Product | rating.product_id | product.id | CASCADE | Xóa sản phẩm → xóa đánh giá |
| ProductRating → User | rating.user_id | user.id | CASCADE | Xóa user → xóa đánh giá |
| Order → User | order.user_id | user.id | CASCADE | Xóa user → xóa đơn hàng |
| OrderItem → Order | orderitem.order_id | order.id | CASCADE | Xóa đơn → xóa mục đơn |
| OrderItem → Product | orderitem.product_id | product.id | PROTECT | Bảo vệ dữ liệu đã bán |
| Shipment → Order | shipment.order_id | order.id | CASCADE | Xóa đơn → xóa vận chuyển (1:1) |

---

## ✅ Ràng Buộc Logic

### **1. Constraint Duy Nhất:**
- `Brand.name` - Tên thương hiệu duy nhất
- `Category.name` - Tên danh mục duy nhất
- `Product.sku` - Mã SKU duy nhất
- `Product(brand, name)` - Không lặp tên sản phẩm cùng brand
- `CartItem(user, product)` - Một sản phẩm một lần trong giỏ
- `ProductRating(product, user)` - Một user một đánh giá cho một sản phẩm
- `OrderItem(order, product)` - Không lặp sản phẩm trong một đơn hàng
- `Shipment.tracking_number` - Mã vận chuyển duy nhất

### **2. Constraint Check:**
- `Product.price` ≥ 0 (Giá không âm)
- `Product.discount_price < Product.price` (Giá chiết khấu phải nhỏ hơn giá gốc)
- `Product.stock` ≥ 0 (Tồn kho không âm)
- `Product.warranty_months` ≥ 1 (Bảo hành tối thiểu 1 tháng)
- `CartItem.quantity` ≥ 1 (Số lượng tối thiểu 1)
- `Order.total_amount` ≥ 0 (Tổng tiền không âm)
- `OrderItem.quantity` ≥ 1 (Số lượng tối thiểu 1)
- `OrderItem.price` ≥ 0 (Giá bán không âm)
- `ProductRating.rating` ∈ [1,5] (Đánh giá 1-5 sao)

### **3. Dữ liệu Lịch Sử:**
- `Product.created_at`, `updated_at` - Theo dõi khi nào sản phẩm được tạo/cập nhật
- `Order.created_at`, `updated_at` - Theo dõi thời gian đặt và cập nhật đơn hàng
- `Shipment.actual_delivery` - Ghi lại thời gian giao thực tế

---

## 🎯 Lợi Ích Của Thiết Kế

✅ **Tính Toàn Vẹn Dữ Liệu:** Khóa ngoại, ràng buộc duy nhất, ràng buộc check

✅ **Tránh Trùng Lặp:** Brand, Category tách riêng

✅ **Linh Hoạt:** Dễ mở rộng (có thể thêm bảng Supplier, Warehouse, ...)

✅ **Hiệu Suất:** Đánh chỉ mục trên khóa chính/ngoại

✅ **Kiên Cố:** `ON_DELETE=PROTECT` để bảo vệ dữ liệu quan trọng

✅ **Tracking:** Lưu giá bán cũ trong OrderItem, không bị ảnh hưởng thay đổi giá

✅ **Quản Lý Vận Chuyển:** Shipment tách riêng, dễ theo dõi

---

## 🚀 Hướng Phát Triển

Có thể mở rộng: Supplier, Warehouse, Inventory, Payment, Return, Customer Review, ...

