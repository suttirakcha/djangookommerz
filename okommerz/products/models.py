from django.db import models
from .countries import COUNTRY_CHOICE
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.

PROMOTION_TYPE_CHOICE = (
    ('Discount', 'Discount'),
    ('Coupon', 'Coupon')
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

CUSTOMER_TYPE_CHOICES = (
    ('Company', 'Company'),
    ('Individual', 'Individual'),
    ('Proprietorship', 'Proprietorship'),
    ('Partnership', 'Partnership')
)

SALES_CHANNELS = (
    ('Website', 'Website'),
    ('Shopee', 'Shopee'),
    ('Lazada', 'Lazada'),
    ('Aliexpress', 'Aliexpress'),
    ('TikTok Shop', 'TikTok Shop'),
    ('Other', 'Other')
)

class Coupon(models.Model):
    coupon_name = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=255)
    coupon_description = models.TextField()
    discount = models.IntegerField(default=0)
    valid_from = models.DateField()
    valid_to = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.coupon_name

class ProductCategory(models.Model):
    category = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Product categories"

    def __str__(self):
        return self.category

class ProductItem(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.IntegerField(default=1)
    product_category = models.ForeignKey(ProductCategory, related_name='product_name', on_delete=models.CASCADE, null=True)
    regular_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    sales_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    product_image = models.ImageField(upload_to='', blank=True, null=True)
    additional_detail = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def clean(self):
        if self.sales_price and self.sales_price > self.regular_price:
            raise ValidationError('Sales price cannot be greater than regular price')

class Address(models.Model):
    address_title = models.CharField(max_length=255)
    address = models.TextField()
    city_or_county = models.CharField(max_length=255)
    state_or_province = models.CharField(max_length=255)
    country = models.CharField(max_length=255, choices=COUNTRY_CHOICE, default='Thailand')
    postal_code = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.address_title

class MarketingCampaign(models.Model):
    campaign_name = models.CharField(max_length=255)
    campaign_description = models.TextField()
    campaign_image = models.ImageField(upload_to='okommerz', blank=True, null=True)

    def __str__(self):
        return self.campaign_name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product} for {self.user.username}"

class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_birth = models.DateField()
    customer_type = models.CharField(max_length=255,choices=CUSTOMER_TYPE_CHOICES,default=1)
    gender = models.CharField(max_length=255,choices=GENDER,blank=True,null=True)

    def __str__(self):
        return self.customer_name


class SalesInvoice(models.Model):
    order_id = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_address = models.TextField()
    sales_channel = models.CharField(max_length=255, choices=SALES_CHANNELS, default=1)
    items = models.ManyToManyField(ProductItem)
