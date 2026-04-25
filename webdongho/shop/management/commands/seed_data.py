from django.core.management.base import BaseCommand
from shop.models import Category, Product, Brand


class Command(BaseCommand):
    help = 'Load seed data for watch shop'

    def handle(self, *args, **options):
        # Create Brands
        brands_data = [
            {'name': 'Rolex', 'country': 'Switzerland', 'founded_year': 1905},
            {'name': 'Omega', 'country': 'Switzerland', 'founded_year': 1848},
            {'name': 'TAG Heuer', 'country': 'Switzerland', 'founded_year': 1860},
            {'name': 'Patek Philippe', 'country': 'Switzerland', 'founded_year': 1839},
            {'name': 'IWC', 'country': 'Switzerland', 'founded_year': 1868},
            {'name': 'Cartier', 'country': 'France', 'founded_year': 1847},
            {'name': 'Seiko', 'country': 'Japan', 'founded_year': 1881},
            {'name': 'Casio', 'country': 'Japan', 'founded_year': 1957},
            {'name': 'Orient', 'country': 'Japan', 'founded_year': 1945},
        ]
        
        brands = {}
        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=brand_data['name'],
                defaults=brand_data
            )
            brands[brand.name] = brand
            if created:
                self.stdout.write(f'✓ Created brand: {brand.name}')
        
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
                self.stdout.write(f'✓ Created category: {name}')
        
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
                'warranty_months': 24,
                'sku': 'ROLEX-SUB-001'
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
                'warranty_months': 24,
                'sku': 'OMEGA-SEA-001'
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
                'warranty_months': 24,
                'sku': 'TAG-CAR-001'
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
                'warranty_months': 12,
                'sku': 'SEIKO-PRO-001'
            },
            {
                'name': 'Casio G-Shock GA-110',
                'brand': 'Casio',
                'category': 'Sports',
                'description': 'Đồng hồ Casio G-Shock nổi tiếng với độ bền vượt trội, chống sốc và chống nước. Lý tưởng cho các hoạt động ngoài trời.',
                'price': 2500000,
                'discount_price': 1999999,
                'stock': 20,
                'status': 'available',
                'warranty_months': 12,
                'sku': 'CASIO-GS-001'
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
                'warranty_months': 24,
                'sku': 'PATEK-NAUT-001'
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
                'warranty_months': 24,
                'sku': 'IWC-PILOT-001'
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
                'warranty_months': 24,
                'sku': 'CARTIER-BLEU-001'
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
                'warranty_months': 12,
                'sku': 'ORIENT-AUTO-001'
            },
            {
                'name': 'Timex Weekender Casual',
                'brand': None,
                'category': 'Casual',
                'description': 'Timex Weekender - đồng hồ casual đơn giản nhưng chắc chắn. Với dây vải nhung thoải mái và mặt số sạch sẽ.',
                'price': 1500000,
                'discount_price': None,
                'stock': 25,
                'status': 'available',
                'warranty_months': 12,
                'sku': 'TIMEX-WEEK-001'
            },
        ]
        
        for prod_data in products_data:
            category = categories[prod_data.pop('category')]
            brand_name = prod_data.pop('brand')
            brand = brands.get(brand_name) if brand_name else brands.get('Omega')  # Default brand
            
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={**prod_data, 'category': category, 'brand': brand}
            )
            if created:
                self.stdout.write(f'✓ Created product: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Seed data loaded successfully!'))
