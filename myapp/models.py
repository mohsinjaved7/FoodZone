from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=35)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    added_to = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Table"


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profiles/%Y/%m/%d', null=True,blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iconimg = models.ImageField(upload_to="icon",default="", null=False)
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Sub_category(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subicon = models.ImageField(upload_to="subicon", default="", null=False)

    def __str__(self):
        return self.name
class Dish(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='dishes/%Y/%m/%d')
    ingredients = models.TextField(null=True)
    details = models.TextField(blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE, null=True)
    price = models.FloatField()
    discounted_price = models.FloatField(blank=True,null=True)
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural ="Dish Table"


class Team(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to="team")
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(Dish, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    invoice_id = models.CharField(max_length=100, blank=True)
    payer_id = models.CharField(max_length=100, blank=True)
    ordered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.user.first_name

    class Meta:
        verbose_name_plural = "Order Table"


class Booking_table(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    contact = models.CharField(max_length=15)
    date = models.DateTimeField(auto_created=True)
    time = models.CharField(max_length=10, null=False , default="")
    guests = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Booking Table"
