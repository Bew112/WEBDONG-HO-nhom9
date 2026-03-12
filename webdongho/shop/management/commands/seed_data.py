from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = 'Load seed data for watch shop'

    def handle(self, *args, **options):
        # Create Categories
        categories_data = [
            ('Luxury', 'Đồng hồ hạng sang'),
            ('Sports', 'Đồng hồ thể thao'),
            ('Casual', 'Đồng hồ casual'),
            ('Dress', 'Đồng hồ lịch sự'),
        ]
        
        categories = {}
        for name, desc in categories_data:
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            categories[name] = cat
            if created:
                self.stdout.write(f'Created category: {name}')
        
        # Create Products
        products_data = [
            {
                'name': 'Rolex Submariner Classic',
                'brand': 'Rolex',
                'category': 'Luxury',
                'description': 'Đồng hồ Rolex Submariner kinh điển với vỏ thép không gỉ, mặt số đen, khả năng chống nước 300m. Là biểu tượng của sang trọng và độ tin cậy.',
                'price': 85000000,
                'discount_price': 75000000,
                'stock': 5,
                'status': 'available',
                'image': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=500&h=500&fit=crop'
            },
            {
                'name': 'Omega Seamaster 300M',
                'brand': 'Omega',
                'category': 'Luxury',
                'description': 'Omega Seamaster là sự lựa chọn hoàn hảo cho những người yêu thích đồng hồ thể thao. Với khả năng chống nước 300m và thiết kế thanh lịch.',
                'price': 45000000,
                'discount_price': 40000000,
                'stock': 3,
                'status': 'available',
                'image': 'https://images.unsplash.com/photo-1547996160-81dac51a7d13?w=500&h=500&fit=crop'
            },
            {
                'name': 'TAG Heuer Carrera',
                'brand': 'TAG Heuer',
                'category': 'Sports',
                'description': 'Đồng hồ TAG Heuer Carrera - sự kết hợp hoàn hảo giữa hiệu năng và phong cách. Được thiết kế cho những người đam mê tốc độ.',
                'price': 35000000,
                'discount_price': 30000000,
                'stock': 7,
                'status': 'available',
                'image': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=500&h=500&fit=crop'
            },
            {
                'name': 'Seiko Prospex Diver',
                'brand': 'Seiko',
                'category': 'Sports',
                'description': 'Seiko Prospex là dòng đồng hồ lặn chuyên nghiệp với độ chính xác cao và khả năng chống nước ấn tượng.',
                'price': 8000000,
                'discount_price': 7000000,
                'stock': 15,
                'status': 'available',
                'image': 'https://images.unsplash.com/photo-1602088113235-229c19758e9f?w=500&h=500&fit=crop'
            },
            {
                'name': 'Casio G-Shock',
                'brand': 'Casio',
                'category': 'Sports',
                'description': 'Đồng hồ Casio G-Shock nổi tiếng với độ bền vượt trội, chống sốc và chống nước. Lý tưởng cho các hoạt động ngoài trời.',
                'price': 2500000,
                'discount_price': 1999999,
                'stock': 20,
                'status': 'available',
                'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop'
            },
            {
                'name': 'Patek Philippe Nautilus',
                'brand': 'Patek Philippe',
                'category': 'Luxury',
                'description': 'Patek Philippe Nautilus - một trong những đồng hồ quý hiếm nhất thế giới. Thiết kế độc đáo và sự hiếm có khiến nó vô cùng quý báu.',
                'price': 150000000,
                'discount_price': 135000000,
                'stock': 1,
                'status': 'available',
                'image': 'https://images.unsplash.com/photo-1548113682-eac2b68bb56e?w=500&h=500&fit=crop'
            },
            {
                'name': 'IWC Pilot Chronograph',
                'brand': 'IWC',
                'category': 'Dress',
                'description': 'IWC Pilot Chronograph - đồng hồ được thiết kế cho các phi công. Chính xác, đáng tin cậy và có thiết kế cổ điển.',
                'price': 55000000,
                'discount_price': 48000000,
                'stock': 4,
                'status': 'available',
                'image': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=500&h=500&fit=crop'
            },
            {
                'name': 'Cartier Ballon Bleu',
                'brand': 'Cartier',
                'category': 'Dress',
                'description': 'Cartier Ballon Bleu với thiết kế sang trọng và thanh lịch. Là lựa chọn hoàn hảo cho những dịp quan trọng.',
                'price': 65000000,
                'discount_price': 58000000,
                'stock': 2,
                'status': 'available',
                'image': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=500&h=500&fit=crop'
            },
            {
                'name': 'Orient Automatic Classic',
                'brand': 'Orient',
                'category': 'Casual',
                'description': 'Orient Automatic - đồng hồ cơ tinh xảo với giá hợp lý. Phù hợp cho người mới bắt đầu sưu tập đồng hồ.',
                'price': 3500000,
                'discount_price': 2999999,
                'stock': 12,
                'status': 'available',
                'image': 'https://images.unsplash.com/photo-1625305288331-ac8f1b1212e1?w=500&h=500&fit=crop'
            },
            {
                'name': 'Timex Weekender',
                'brand': 'Other',
                'category': 'Casual',
                'description': 'Timex Weekender - đồng hồ casual đơn giản nhưng chắc chắn. Với dây vải nhung thoải mái và mặt số sạch sẽ.',
                'price': 1500000,
                'discount_price': None,
                'stock': 25,
                'status': 'available',
                'image': 'https://images.unsplash.com/photo-1542972062-e5c36664baf8?w=500&h=500&fit=crop'
            },
        ]
        
        for prod_data in products_data:
            category = categories[prod_data.pop('category')]
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={**prod_data, 'category': category}
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('✓ Seed data loaded successfully!'))
