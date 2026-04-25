# ✅ Báo Cáo Thiết Kế Cơ Sở Dữ Liệu - Watch Shop

## 📌 Tóm Tắt Thay Đổi

Cơ sở dữ liệu đã được thiết kế lại với **7 bảng chính** có quan hệ chặt chẽ, đáp ứng đầy đủ các yêu cầu:
- ✅ **Ít nhất 5 bảng** - Có **7 bảng chính**
- ✅ **Có quan hệ** - Nhiều Foreign Key (FK) và One-to-One
- ✅ **Khóa chính/khóa ngoại rõ ràng** - Tất cả FK được định nghĩa
- ✅ **Ràng buộc logic chặt chẽ** - Unique constraints, NOT NULL, Min/Max validators

---

## 📊 Các Bảng Dữ Liệu

### 1. **Brand** (Thương Hiệu) - **MỚI**
- Lưu trữ thông tin thương hiệu đồng hồ (Rolex, Omega, ...)
- Tách riêng từ Product để tránh dữ liệu trùng lặp
- Hỗ trợ thêm thông tin chi tiết: quốc gia, năm thành lập, logo

### 2. **Category** (Danh Mục) - Cải Thiện
- Phân loại sản phẩm theo loại (Luxury, Sports, Casual, Dress)
- Giữ nguyên cấu trúc nhưng bổ sung ràng buộc duy nhất

### 3. **Product** (Sản Phẩm) - Cải Thiện Đáng Kể
- **Thay Đổi:** Brand từ CharField → ForeignKey(Brand)
- Thêm `SKU` (mã sản phẩm) duy nhất
- Thêm `warranty_months` - thời gian bảo hành
- Thêm `pre_order` status
- Constraint: `unique_together(brand, name)` - Không sản phẩm trùng tên cùng brand

### 4. **ProductRating** (Đánh Giá Sản Phẩm) - **MỚI**
- Cho phép khách hàng đánh giá sản phẩm
- Lưu trữ score (1-5 sao) và comment
- Constraint: `unique_together(product, user)` - Mỗi user đánh giá 1 lần/sản phẩm

### 5. **CartItem** (Giỏ Hàng) - Cải Thiện
- Thêm `updated_at` field
- Constraint: `unique_together(user, product)` - Tránh mục trùng lặp
- Thêm method `get_total_price()`

### 6. **Order** (Đơn Hàng) - Cải Thiện Đáng Kể
- **Status mới:** pending → confirmed → shipping → delivered (thay vì pending → approved → rejected)
- Thêm `email` field
- Thêm `notes` field cho ghi chú khách hàng
- Cập nhật status choices phù hợp hơn

### 7. **OrderItem** (Chi Tiết Đơn Hàng) - Cải Thiện
- Thêm constraint: `unique_together(order, product)` - Tránh sản phẩm trùng lặp
- Thêm method `get_subtotal()`
- `ON_DELETE=PROTECT` để bảo vệ dữ liệu đã bán

### 8. **Shipment** (Vận Chuyển) - **MỚI**
- Theo dõi vận chuyển đơn hàng
- One-to-One relationship với Order
- Lưu thông tin: hãng vận chuyển, mã tracking, ngày giao dự kiến/thực tế
- Status: pending → picked_up → in_transit → out_for_delivery → delivered

---

## 🔄 Quan Hệ Giữa Các Bảng

```
┌──────────┐
│   User   │ (Django built-in)
└────┬─────┘
     │
     ├─ (1:M) CartItem
     ├─ (1:M) Order
     └─ (1:M) ProductRating

┌───────────┐         ┌──────────┐
│  Brand    │←────────│ Product  │
│ (unique)  │ (1:M)   │          │
└───────────┘         └────┬─────┘
                           │
                ┌──────────┼──────────┐
                │          │          │
            CartItem  ProductRating  OrderItem
                │          │          │
                └──────────┴──────────┤
                                     │
                                 Order
                                  │
                                  │ (1:1)
                                  │
                              Shipment

┌──────────────┐
│  Category    │ ──(1:M)──│ Product
└──────────────┘
```

---

## ✅ Ràng Buộc Logic

### Unique Constraints:
- Brand.name
- Category.name
- Product.sku
- Product(brand, name)
- CartItem(user, product)
- ProductRating(product, user)
- OrderItem(order, product)
- Shipment.tracking_number

### Check Constraints (Validators):
- Product.price ≥ 0
- Product.discount_price < Product.price
- Product.stock ≥ 0
- Product.warranty_months ≥ 1
- CartItem.quantity ≥ 1
- Order.total_amount ≥ 0
- OrderItem.quantity ≥ 1
- OrderItem.price ≥ 0
- ProductRating.rating ∈ [1,5]

### Foreign Key Protection:
- Product → Brand: `ON_DELETE=PROTECT` (bảo vệ brand từ bị xóa)
- Product → Category: `ON_DELETE=CASCADE` (xóa danh mục → xóa sản phẩm)
- OrderItem → Product: `ON_DELETE=PROTECT` (bảo vệ dữ liệu bán)
- Order → Shipment: `ON_DELETE=CASCADE` (xóa đơn → xóa vận chuyển)

---

## 📝 Files Đã Thay Đổi/Tạo

### ✏️ Cập Nhật:
1. **shop/models.py** - Thiết kế lại 7 bảng
2. **shop/views.py** - Cập nhật import, thay `brand__icontains` → `brand__name__icontains`
3. **shop/admin.py** - Thêm BrandAdmin, ProductRatingAdmin, ShipmentAdmin
4. **templates/shop/base.html** - Sửa form tìm kiếm header
5. **templates/shop/product_list.html** - Tách form tìm kiếm và lọc riêng
6. **shop/management/commands/seed_data.py** - Cập nhật tạo Brand, thêm dữ liệu mới

### 🆕 Tạo:
1. **shop/migrations/0001_initial.py** - Migration cho schema mới
2. **DATABASE_DESIGN.md** - Tài liệu thiết kế cơ sở dữ liệu chi tiết
3. **DATABASE_SUMMARY.md** - File này

---

## 📊 Dữ Liệu Khởi Tạo (Seed Data)

Đã tạo:
- ✅ **9 thương hiệu**: Rolex, Omega, TAG Heuer, Patek Philippe, IWC, Cartier, Seiko, Casio, Orient
- ✅ **4 danh mục**: Luxury, Sports, Casual, Dress
- ✅ **10 sản phẩm**: Từ các thương hiệu khác nhau, với giá ≥ 0 và discount < price

---

## 🚀 Hướng Phát Triển

Có thể mở rộng thêm:
- ❓ **Supplier** - Quản lý nhà cung cấp
- ❓ **Warehouse** - Quản lý kho
- ❓ **Inventory** - Quản lý tồn kho chi tiết
- ❓ **Payment** - Quản lý thanh toán
- ❓ **Return** - Quản lý hoàn trả
- ❓ **Promotion/Discount** - Khuyến mãi
- ❓ **Customer Address** - Lưu địa chỉ giao hàng đã dùng

---

## ✨ Lợi Ích Của Thiết Kế Mới

### Tính Toàn Vẹn Dữ Liệu 🔐
- FK constraints bảo vệ dữ liệu
- Unique constraints tránh dữ liệu trùng
- Check constraints kiểm tra logic

### Tránh Trùng Lặp 🎯
- Brand tách riêng (không lặp tên thương hiệu)
- Category tách riêng
- SKU duy nhất cho từng sản phẩm

### Linh Hoạt & Mở Rộng 📈
- Dễ thêm thông tin brand (logo, quốc gia, ...)
- Dễ thêm giá trị đánh giá
- Dễ theo dõi vận chuyển

### Hiệu Suất 🚄
- FK tự động tạo index
- Primary key tối ưu
- Queries hiệu quả

### Quản Lý Tốt 👌
- Lưu giá bán trong OrderItem (không bị thay đổi nếu sửa product)
- Lưu warranty info
- Lưu actual_delivery date

---

## ✅ Kiểm Chứng

- [x] Migrations tạo thành công
- [x] Database migrate successfully
- [x] Seed data đã tải
- [x] Admin panel cập nhật
- [x] Views hoạt động với Brand FK
- [x] Tìm kiếm sản phẩm theo brand name
- [x] Django check passed

---

## 📚 Tài Liệu Thêm

Xem chi tiết: **DATABASE_DESIGN.md**

