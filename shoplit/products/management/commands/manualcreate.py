from django.core.management.base import BaseCommand, CommandError
from products.models import Category, SubCategory, Product

class Command(BaseCommand):
    help = "create new set of categories, subcategories, and products"

    def add_arguments(self, parser):
        parser.add_argument('num_categories', type=int, help='Number of categories')
        parser.add_argument('num_subcategories', type=int, help='Number of subcategories per category')
        parser.add_argument('num_products', type=int, help='Number of products per subcategory')
        parser.add_argument("--show-total", action='store_true', default=False)

    def handle(self, *args, **options):
        category_count = int(options.get('num_categories'))