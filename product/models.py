from django.db import models
from account.models import Customer, CustomUser
from django.core.validators import RegexValidator

# Create your models here.
class Category(models.Model):
    name =  models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    stock_qty = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_pics/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    
class ProductWeightPrice(models.Model):
    WEIGHT_CHOICES = [
        ('250g', '250 grams'),
        ('500g', '500 grams'),
        ('1kg', '1 kilogram'),
        ('2kg', '2 kilograms'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='weight_prices')
    weight = models.CharField(max_length=10, choices=WEIGHT_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} - {self.weight} - ${self.price}"
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state= models.CharField(max_length=50)
    pincode = models.CharField(max_length=6,validators=[RegexValidator(r'^\d{6}$','Enter a valid 6 digit pincode')])


class Order(models.Model):
    order_id = models.CharField(max_length=50,primary_key=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)

    shipping_address = models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL, null=True, blank=True)

    payment_status = models.CharField(max_length=20,choices=(('paid','Paid'),('unpaid','Unpaid')),default='unpaid')

    order_status = models.CharField(max_length=20,choices=(('pending','Pending'),('shipped','Shipped'),('delivered','Delivered')),default='pending')

    order_amount= models.DecimalField(max_digits=10,decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.CharField(max_length=10) 
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        
        product_weight_price = ProductWeightPrice.objects.get(product=self.product, weight=self.weight)
        self.unit_price = product_weight_price.price
        super().save(*args, **kwargs)
        
        def __str__(self):
            return f"{self.product.title} ({self.weight}) - Order: {self.order}"




class Vegetable(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WeeklyBasket(models.Model):
    BASKET_CHOICES = [
        ('small', 'Small Basket - $10'),
        ('medium', 'Medium Basket - $20'),
        ('large', 'Large Basket - $30'),
    ]
    basket_type = models.CharField(max_length=10, choices=BASKET_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.get_basket_type_display()
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=1)
    product_weight_price = models.ForeignKey(ProductWeightPrice, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.title} ({self.weight})"
from django.contrib.auth.models import User  
class PaymentPlan(models.Model):
    name = models.CharField(max_length=100) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()  
    description = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.name} - ₹{self.price} ({self.duration_days} days)"
from django.conf import settings

class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.payment_plan.name if self.payment_plan else 'No Plan'}"

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    invoice_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=(('paid', 'Paid'), ('unpaid', 'Unpaid')), default='unpaid')
    
    

    def __str__(self):
        return f"Invoice {self.id} - Order {self.order.order_id}"

