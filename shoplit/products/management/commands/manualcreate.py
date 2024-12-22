from django.core.management.base import BaseCommand, CommandError
from products.models import Category, SubCategory, Product
from products import utils
class Command(BaseCommand):
    help = "create new set of categories, subcategories, and products"

    def add_arguments(self, parser):
        # parser.add_argument('num_categories', type=int, help='Number of categories')
        # parser.add_argument('num_subcategories', type=int, help='Number of subcategories per category')
        parser.add_argument('num_products', type=int, help='Number of products per subcategory')
        parser.add_argument("--categories", action='store_true', default=False)
        parser.add_argument("--products", action='store_true', default=False)

    def handle(self, *args, **options):
        create_categories = options.get('categories')
        create_products = options.get('products')
        products = options.get('num_products')
        if create_categories:
            utils.generate_categories()
        if create_products:
            utils.generate_products(num=products)