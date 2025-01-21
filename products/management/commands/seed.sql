-- Ensure the database is selected
USE ecommerce_db;

-- Insert sample data into the Category table
INSERT INTO category (id, name, description, created_at, updated_at)
VALUES 
    (UUID(), 'Electronics', 'Devices and gadgets', NOW(), NOW()),
    (UUID(), 'Fashion', 'Clothing and accessories', NOW(), NOW()),
    (UUID(), 'Home Appliances', 'Appliances for home use', NOW(), NOW());

-- Retrieve the IDs of the categories for further use
SELECT * FROM category;

-- Insert sample data into the SubCategory table
INSERT INTO subcategory (id, category_id, name, description, created_at, updated_at)
VALUES 
    (UUID(), (SELECT id FROM category WHERE name = 'Electronics'), 'Mobile Phones', 'Smartphones and accessories', NOW(), NOW()),
    (UUID(), (SELECT id FROM category WHERE name = 'Electronics'), 'Laptops', 'Portable computers', NOW(), NOW()),
    (UUID(), (SELECT id FROM category WHERE name = 'Fashion'), 'Men\'s Wear', 'Clothing for men', NOW(), NOW()),
    (UUID(), (SELECT id FROM category WHERE name = 'Home Appliances'), 'Kitchen Appliances', 'Appliances for the kitchen', NOW(), NOW());

-- Retrieve the IDs of the subcategories for further use
SELECT * FROM subcategory;

-- Insert sample data into the Product table
INSERT INTO product (id, name, description, price, stock_quantity, vendor_id, category_id, subcategory_id, is_active, created_at, updated_at)
VALUES 
    (UUID(), 'iPhone 14', 'Latest Apple smartphone', 999.99, 50, VENDOR_ID, 
        (SELECT id FROM category WHERE name = 'Electronics'), 
        (SELECT id FROM subcategory WHERE name = 'Mobile Phones'), 
        TRUE, NOW(), NOW()),
    (UUID(), 'Dell XPS 13', 'Compact and powerful laptop', 1199.99, 30, VENDOR_ID, 
        (SELECT id FROM category WHERE name = 'Electronics'), 
        (SELECT id FROM subcategory WHERE name = 'Laptops'), 
        TRUE, NOW(), NOW()),
    (UUID(), 'Men\'s T-Shirt', '100% cotton casual wear', 19.99, 100, VENDOR_ID, 
        (SELECT id FROM category WHERE name = 'Fashion'), 
        (SELECT id FROM subcategory WHERE name = 'Men\'s Wear'), 
        TRUE, NOW(), NOW()),
    (UUID(), 'Blender Pro', 'High-performance kitchen blender', 49.99, 75, VENDOR_ID, 
        (SELECT id FROM category WHERE name = 'Home Appliances'), 
        (SELECT id FROM subcategory WHERE name = 'Kitchen Appliances'), 
        TRUE, NOW(), NOW());

-- Retrieve the IDs of the products for further use
SELECT * FROM product;

-- Insert sample data into the ProductImage table
INSERT INTO productimage (id, product_id, image)
VALUES 
    (UUID(), (SELECT id FROM product WHERE name = 'iPhone 14'), 'https://res.cloudinary.com/example/image/upload/iphone14.jpg'),
    (UUID(), (SELECT id FROM product WHERE name = 'Dell XPS 13'), 'https://res.cloudinary.com/example/image/upload/dell_xps13.jpg'),
    (UUID(), (SELECT id FROM product WHERE name = 'Men\'s T-Shirt'), 'https://res.cloudinary.com/example/image/upload/mens_tshirt.jpg'),
    (UUID(), (SELECT id FROM product WHERE name = 'Blender Pro'), 'https://res.cloudinary.com/example/image/upload/blender_pro.jpg');

-- Validate the inserted data
SELECT * FROM productimage;
