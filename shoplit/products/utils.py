from mimesis import Generic
from mimesis.locales import Locale
from faker import Faker
# from mimesis.builtins import Commerce

import random
# from products.models import Category, SubCategory, Product

# Initialize Mimesis

#company, finance, food.dish, food.drink, food.fruit, food.species, hardware.graphics, hardware.phone_model
#hardware.cpu_codeame, 
generic = Generic(locale=Locale.EN)
commerce = generic

# print(commerce)from faker import Faker
from faker_commerce import Provider

fake = Faker()
fake.add_provider(Provider)

# Generate products and categories
print(fake.ecommerce_name())  # Random product name
print(fake.ecommerce_category())  # Random category name
# print(fake.ecommerce_color())  # Random color
# print(fake.ecommerce_department())  # Random department/


# # Generate categories
# def generate_categories(num=5):
#     print('hey')
#     categories = []
#     for _ in range(num):
#         category_name = commerce.department()  # E-commerce department names
#         # category, created = Category.objects.get_or_create(name=category_name)
#         categories.append(category_name)
#     return categories

# # Generate subcategories
# def generate_subcategories(categories, num=3):
#     subcategories = []
#     for category in categories:
#         for _ in range(num):
#             subcategory_name = commerce.category()  # Subcategories from e-commerce domains
#             # subcategory, created = SubCategory.objects.get_or_create(
#             #     name=subcategory_name,
#             #     category=category
#             # )
#             subcategories.append(subcategory_name)
#     return subcategories

# # Generate products
# def generate_products(subcategories, num=10):
#     for subcategory in subcategories:
#         products = []
#         for _ in range(num):
#             product_name = commerce.product_name()  # Random product names
#             price = round(random.uniform(10, 1000), 2)
#             stock_quantity = random.randint(1, 100)
#             # Product.objects.create(
#             #     name=product_name,
#             #     subcategory=subcategory,
#             #     price=price,
#             #     stock_quantity=stock_quantity,
#             #     description=generic.text.text(quantity=1)  # Random product description
#             # )
#             products.append(product_name)
#     return products

# # Run the script
# def seed_database():
#     print("Seeding database with e-commerce terms...")
#     categories = generate_categories(num=5)
#     subcategories = generate_subcategories(categories, num=3)
#     generate_products(subcategories, num=10)
#     print("Database seeded successfully!")

# # Call this function to seed your data
# seed_database()


# # print(generate_categories())