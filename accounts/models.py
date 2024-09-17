from django.db import models
from django.contrib.auth.models import User


# CUSTOMER MODEL
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=20, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="download1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return self.name
	# def __str__(self):
    #     # Return a fallback string if name is None
	# 	return self.name if self.name else "Unnamed Customer"

	@property
	def orders(self):
		order_count = self.order_set.all().count()
		return str(order_count)


class Manufacturer(models.Model):
    name = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    established_date = models.DateField(null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name


class Product(models.Model):

	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			) 

	name = models.CharField(max_length=200, null=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.TextField(null=True)
	release_date = models.DateField(null=True)
	manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			) 

	customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete= models.SET_NULL, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return str(self.product)