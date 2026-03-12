#!/bin/bash
# WatchShop - Quick Start Script
# Hướng dẫn chạy website nhanh nhất

echo "🚀 WatchShop - Bắt Đầu Nhanh"
echo "================================"
echo ""

# Check Python
echo "✓ Kiểm tra Python..."
python --version

# Check Django
echo "✓ Kiểm tra Django..."
python -m django --version

# Activate venv (if exists)
if [ -d "venv" ]; then
    echo "✓ Kích hoạt virtual environment..."
    source venv/bin/activate
fi

# Install requirements
echo "✓ Cài đặt dependencies..."
pip install -r requirements.txt

# Migrations
echo "✓ Tạo database..."
python manage.py migrate

# Seed data
echo "✓ Load dữ liệu mẫu..."
python manage.py seed_data

# Create admin (optional)
read -p "Bạn có muốn tạo tài khoản admin? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

echo ""
echo "✅ Hoàn thành! Khởi động server..."
echo ""
echo "Server sẽ chạy tại: http://127.0.0.1:8000/"
echo "Admin panel: http://127.0.0.1:8000/admin/"
echo ""
python manage.py runserver
