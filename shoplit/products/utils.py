from faker import Faker
from random import randint, uniform

import sys
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shoplit.settings")
django.setup()

from products.models import Category, SubCategory, Product

#company, finance, food.dish, food.drink, food.fruit, food.species, hardware.graphics, hardware.phone_model
#hardware.cpu_codeame, 

fake = Faker()

categories = [
    "Electronics", "Fashion", "Home & Garden", "Health & Beauty", "Toys & Hobbies", 
    "Sporting Goods", "Automotive", "Books", "Music", "Movies & TV", "Collectibles", 
    "Industrial & Scientific", "Real Estate", "Food & Beverages", "Baby", "Arts & Crafts", 
    "Pet Supplies"
]

subcategories = {
    "Electronics": [
        "Mobile Phones", "Laptops", "Tablets", "Wearables", "Headphones", "Cameras", 
        "TVs & Home Entertainment", "Gaming Consoles", "Computer Components", "Smart Home Devices", 
        "Drones", "Virtual Reality"
    ],
    "Fashion": [
        "Men's Clothing", "Women's Clothing", "Shoes", "Jewelry", "Watches", "Bags & Luggage", 
        "Sunglasses", "Accessories", "Kids' Clothing", "Activewear", "Outerwear", "Swimwear", 
        "Underwear & Lingerie", "Clothing Sets"
    ],
    "Home & Garden": [
        "Furniture", "Kitchen & Dining", "Bedding", "Garden & Outdoor", "Home Improvement", 
        "Home Décor", "Lighting", "Storage & Organization", "Rugs & Carpets", "Curtains & Blinds", 
        "Heating & Cooling", "Cleaning Supplies", "Appliances"
    ],
    "Health & Beauty": [
        "Skincare", "Makeup", "Hair Care", "Fragrances", "Personal Care", "Vitamins & Supplements", 
        "Fitness Equipment", "Dental Care", "Shaving & Grooming", "Nail Care", "Health Monitors", 
        "Beauty Tools & Devices"
    ],
    "Toys & Hobbies": [
        "Action Figures", "Dolls & Bears", "Games", "Building Toys", "Cars & Remote-Controlled Toys", 
        "Puzzles", "Educational Toys", "Model Kits", "Collectible Card Games", "Arts & Crafts", 
        "Stuffed Animals", "Party Supplies"
    ],
    "Sporting Goods": [
        "Exercise & Fitness", "Outdoor Recreation", "Cycling", "Water Sports", "Team Sports", 
        "Individual Sports", "Winter Sports", "Golf", "Hiking & Camping", "Hunting & Fishing", 
        "Fan Shop", "Sports Apparel"
    ],
    "Automotive": [
        "Car Parts & Accessories", "Tires", "Tools & Equipment", "Interior Accessories", 
        "Exterior Accessories", "Car Care", "Motorcycle Parts", "Boat Parts", "RV Parts", 
        "Car Electronics", "Vehicle Electronics & GPS"
    ],
    "Books": [
        "Fiction", "Non-Fiction", "Textbooks", "Children's Books", "E-books", "Audio Books", 
        "Educational & Learning", "Cookbooks", "Biographies & Memoirs", "Travel", "Graphic Novels", 
        "Comics"
    ],
    "Music": [
        "Vinyl Records", "CDs", "Digital Music", "Musical Instruments", "Sheet Music", 
        "Music Memorabilia", "DJ Equipment", "Karaoke", "Rock", "Pop", "Classical", "Jazz", 
        "Hip-Hop", "Country", "R&B"
    ],
    "Movies & TV": [
        "DVDs", "Blu-ray", "4K UHD", "Movie Memorabilia", "Box Sets", "TV Shows", 
        "Streaming Services", "Movie Posters", "Foreign Films", "Documentaries", "Special Edition"
    ],
    "Collectibles": [
        "Coins", "Stamps", "Trading Cards", "Antiques", "Sports Memorabilia", "Vintage Clothing", 
        "Autographs", "Art", "Figurines", "Historical & Political Memorabilia", "Movie & TV Collectibles"
    ],
    "Industrial & Scientific": [
        "Laboratory Equipment", "Industrial Tools", "Safety Equipment", "Manufacturing & Processing", 
        "Test Instruments", "Electrical Equipment", "Welding & Soldering", "Office Equipment", 
        "HVAC Equipment", "Janitorial Supplies"
    ],
    "Real Estate": [
        "Residential Properties", "Commercial Properties", "Land", "Vacation Homes", "Apartments", 
        "Houses for Sale", "Rentals", "Property Services", "Investment Properties"
    ],
    "Food & Beverages": [
        "Gourmet Food", "Snacks", "Beverages", "Health Food", "Organic", "Coffee", "Tea", "Alcohol", 
        "Spices & Seasonings", "Bakery", "Meal Kits", "Frozen Food"
    ],
    "Baby": [
        "Clothing", "Toys", "Furniture", "Feeding", "Diapering", "Baby Gear", "Baby Safety", 
        "Health & Hygiene", "Strollers", "Car Seats", "Maternity Products", "Nursery Furniture"
    ],
    "Arts & Crafts": [
        "Drawing & Painting", "Crafting Tools", "Sewing & Needlework", "Beading & Jewelry Making", 
        "Scrapbooking", "Paper Crafting", "Art Supplies", "Knitting & Crocheting", "Home Décor", 
        "Fabric & Textile Arts"
    ],
    "Pet Supplies": [
        "Dogs", "Cats", "Birds", "Fish", "Reptiles", "Small Animals", "Pet Food", "Pet Toys", 
        "Pet Grooming", "Pet Health", "Pet Accessories", "Pet Furniture"
    ]
}
def generate_categories():
    for category_name in categories:
        category, created = Category.objects.get_or_create(name=category_name)
        print(f"Category '{category_name}' created with ID: {category.id}")
        generate_subcategories(category)

# Generate subcategories
def generate_subcategories(category):
    subcategory_names = subcategories.get(category.name, [])
    for subcategory_name in subcategory_names:
        subcategory, created = SubCategory.objects.get_or_create(name=subcategory_name, category=category)
        print(f"Subcategory '{subcategory_name}' created under '{category.name}'")


def generate_products(subcategories=subcategories, num=1):
    products = []
    print(f"Generating products {num} per subcategory")
    for category in subcategories:
        for subcategory in subcategories[category]:
            for _ in range(num):
                # Generate fake product details
                product_name = fake.word() 
                price = round(uniform(10, 1000), 2)  
                stock_quantity = randint(1, 100)  
                description = fake.text(max_nb_chars=200)  
                
                # Create the product and save to the database
                try:
                    product = Product(
                        name=product_name,
                        description=description,
                        price=price,
                        stock_quantity=stock_quantity,
                        subcategory=SubCategory.objects.get(name=subcategory),
                        category=SubCategory.objects.get(name=subcategory).category
                    )
                except:
                    pass
                
                products.append(product)
                # print(f"Product updated with {product}")

    Product.objects.bulk_create(products, ignore_conflicts=True)
    
    return products

"""def seed_database():
    print("Seeding database with e-commerce terms...")
    categories = generate_categories(num=5)
    subcategories = generate_subcategories(categories, num=3)
    generate_products(subcategories, num=10)
    print("Database seeded successfully!")

seed_database()"""


# generate_categories()