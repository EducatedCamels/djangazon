from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from sorl.thumbnail import ImageField



options = (
        (0, 'False'),
        (1, 'True'),
)
# Create your models here.

class UserProfile(models.Model):
    """
    purpose: pulls in default user model and creates a UserProfile class
    author: Helana Nosrat
    args:models.Model
    returns: N/A
    """
    user = models.ForeignKey(User)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=12, blank=True)



class Category(models.Model):
    """
    purpose: creates the category table in the database
    author: James Tonkin
    args: models.Model
    returns: N/A
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


    def get_top_three_products(self):
        """
        purpose: creates a top 3 list of products in a product category
        author: Bri Wyatt
        returns: a list of the first three products in the
        category. Each text item is a hyperlink
        that connects to that product's detail page
        """
        return Product.objects.filter(category=self).order_by('-id')[:3]

    def get_products_from_single_cat(self):
        """
        purpose: Pulls all products from a single category
        author: James Tonkin
        returns: a list of products in the
        category. Each text item is a hyperlink
        that connects to that product's detail page
        aruguments: self
        """
        return Product.objects.filter(category=self)


class Product(models.Model):
    """
    purpose: creates the product table in the database
    author: James Tonkin, Bri Wyatt
    args: models.Model
    returns: N/A
    """
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE,
        related_name = 'products'
    )
    seller = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
    title = models.CharField(max_length = 255)
    price = models.DecimalField(max_digits = 19, decimal_places = 2, validators = [MinValueValidator(0.0)])    # Come back to the price field, in order to not allow negative numbers
    description = models.TextField(blank = True, null = True)
    quantity = models.PositiveIntegerField()
    is_local = models.BooleanField(default=False)
    city = models.CharField(max_length = 255, blank = True, null = True)
    photo = models.ImageField(blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

class PaymentType(models.Model):
    """
    purpose: creates the payment type table in the database
    author: James Tonkin
    args: models.Model
    returns: N/A
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 255)
    account_number = models.IntegerField()
    enabled = models.IntegerField(default=1, choices=options)

class Order(models.Model):
    """
    purpose: creates the order table in the database
    author: James Tonkin
    args: models.Model
    returns: N/A
    """
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
    payment_type = models.ForeignKey(
        PaymentType,
        null = True,
        blank = True
    )

class LineItem(models.Model):
    """
    purpose: creates the lineitem table in the database
    author: James Tonkin
    args: models.Model
    returns: N/A
    """
    order = models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        on_delete = models.CASCADE,
    )
