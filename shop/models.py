from django.db import models


# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    pname = models.CharField(max_length=50)
    pdesc = models.CharField(max_length=300)
    pdate = models.DateField()
    prod_price = models.IntegerField(default=0)
    pcategory = models.CharField(max_length=50, default="")
    psubcategory = models.CharField(max_length=50, default="")
    pimage = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.pname


class Contact(models.Model):
    cont_id = models.AutoField(primary_key='True')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key='True')
    item_json = models.CharField(max_length=5000)
    tprice = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.order_id) + self.name


class OrderTrack(models.Model):
    update_id = models.AutoField(primary_key='True')
    order_id = models.IntegerField(default="")
    prod_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id) + self.prod_desc[0:25]
