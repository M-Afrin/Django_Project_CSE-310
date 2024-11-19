from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    account = models.OneToOneField('UserProfile', on_delete=models.CASCADE,related_name='user_account')
    cart = models.OneToOneField('ShoppingCart', on_delete=models.CASCADE,related_name='user_cart',null=True, blank=True)
    seller= models.OneToOneField('UserProfile',on_delete=models.SET_NULL, null=True, blank=True, related_name='user_seller')
    rating= models.FloatField(default=0.0)
    order_history= models.ManyToManyField('Order', blank=True, related_name='user_order_history')
    wishlist= models.ManyToManyField('Product', blank=True, related_name='user_wishlist')

    def __str__(self):
        return f"User: {self.account.name}"
'''
    def place_order(self, order):
        self.order_history.add(order)
        self.save()

    
    def review_product(self, product, review):
        review.product = product
        review.user= self
        review.save()

    def view_order_history(self):
        return self.order_history.all()
    
    def add_to_wishlist(self, product):
        """Adds a product to the user's wishlist."""
        self.wishlist.add(product)

    def remove_from_wishlist(self, product):
        """Removes a product from the user's wishlist."""
        self.wishlist.remove(product)'''


class Product(models.Model):
    productID = models.AutoField(primary_key=True)
    p_name= models.CharField(max_length=100)
    description = models.TextField()
    category= models.CharField(max_length=50)
    size= models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    price= models.DecimalField(max_digits=10, decimal_places=3)
    seller= models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    stock= models.IntegerField()
    discount = models.FloatField(default=0.0)

'''
    def check_availability(self):
        """Check if the product is in stock."""
        return self.stock > 0

    def update_stock(self, quantity):
        """Update the stock after a purchase."""
        if quantity > self.stock:
            raise ValidationError({'stock': "Not enough stock available."})
        self.stock -= quantity
        self.save()

    def apply_discount(self, discount_percentage):
        """Apply a new discount to the product."""
        self.discount = discount_percentage/ 100.0
        self.clean()
        self.save()
    
    def get_final_price(self):
        """
        Calculate the price after applying the discount.
        Returns the final price as a Decimal.
        """
        return self.price * (1 - self.discount)
        

    def __str__(self):
        return self.p_name
    
    def clean(self):
        """Ensure data integrity."""
        if self.stock < 0:
            raise ValidationError({'stock': "Stock cannot be negative."})
        if self.price < 0:
            raise ValidationError({'price': "Price cannot be negative."})
        if not (0.0 <= self.discount <= 1.0):
            raise ValidationError({'discount': "Discount must be between 0.0 and 1.0."})
        
'''
class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    orderDate = models.DateTimeField(auto_now_add=True)
    shippingAddress = models.TextField()
    paymentStatus = models.CharField(max_length=50)  # e.g., "Paid", "Pending"
    orderStatus = models.CharField(max_length=50)  # e.g., "Processing", "Shipped", "Delivered"
    totalAmount = models.FloatField()
    products = models.ManyToManyField(Product, related_name="orders")
'''
    def update_order_status(self, new_status):
        """Update the status of the order."""
        self.orderStatus = new_status
        self.save()

    def calculate_total_amount(self):
        """Calculate the total amount for the order."""
        total = 0
        for product in self.products.all():
            total += product.price * self.quantity
        self.totalAmount = total
        self.save()

    def __str__(self):
        return f"Order {self.orderID} by {self.buyer.username}"
'''
class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # For simplicity; recommended to use Django's auth system for handling passwords securely
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    product_list = models.ManyToManyField(Product, blank=True, related_name='sellers')

    def __str__(self):
        return self.name
'''
    def register(self, name, email, password):
        """Registers a new user profile."""
        self.name = name
        self.email = email
        self.password = password  # In practice, use Django's built-in User model for password hashing
        self.save()

    def login(self, email, password):
        """Simulates user login. Real authentication would use Django's auth system."""
        if self.email == email and self.password == password:
            return True
        return False

    def logout(self):
        """Simulates user logout. In a real application, Django's session system would handle this."""
        pass  # Handle session removal in views

    def update_profile(self, **kwargs):
        """Updates user profile details."""
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
        self.save()

    def delete_account(self):
        """Deletes the user account."""
        self.delete()

    def add_product(self, product):
        """Adds a product to the user's product list."""
        self.product_list.add(product)

    def update_product(self, product, **kwargs):
        """Updates details of a specific product."""
        for field, value in kwargs.items():
            if hasattr(product, field):
                setattr(product, field, value)
        product.save()

    def remove_product(self, product):
        """Removes a product from the user's product list."""
        self.product_list.remove(product)

    def view_sales_report(self):
        """Generates a basic sales report for the user's products."""
        # Placeholder: Implement actual sales logic based on Order model
        return f"Sales report for {self.name}"'''


