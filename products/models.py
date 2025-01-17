from django.db import models
from customuser.models import Vendor
import uuid
from cloudinary.models import CloudinaryField



# Represents a top-level category for classifying products
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "categories"
        indexes = [ models.Index(fields=['name']), ]


# Represents a subcategory under a specific category
class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='subcategories'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('category', 'name')  # Ensures unique subcategories within a category
        verbose_name_plural = "subcategories"
        indexes = [ models.Index(fields=['category', 'name']), ]

    def __str__(self):
        return f"{self.category.name} - {self.name}"


# Represents a product with details such as name, price, and stock level
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='products'
    )
    subcategory = models.ForeignKey(
        'SubCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='products'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'subcategory')
        indexes = [ models.Index(fields=['name']), 
                   models.Index(fields=['category']), 
                   models.Index(fields=['subcategory']), 
                   models.Index(fields=['price']), 
                   models.Index(fields=['created_at']), ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Automatically sets the category based on the subcategory before saving.
        """
        if self.subcategory and self.subcategory.category:
            self.category = self.subcategory.category
        super().save(*args, **kwargs)

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0
        return reviews.aggregate(models.Avg('rating'))['rating__avg']
    
    @property
    def review_count(self):
        return self.reviews.count()
    
    def reduce_stock(self, quantity):
        if quantity > self.stock_quantity:
            raise ValueError("Insufficient stock")
        self.stock_quantity -= quantity
        self.save()

    def increase_stock(self, quantity):
        self.stock_quantity += quantity
        self.save()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)  # Establish one-to-many relationship
    image = CloudinaryField('image')

    def __str__(self):
        return f"Image for {self.product.name}"