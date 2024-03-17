from calendar import c
from turtle import mode
from django.db import models
import string
import json
import random
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import receiver

class Users(AbstractUser):
    USER = (
        (1,1),
        (2,2),
        (3,3),
    )
    user_id = models.BigAutoField(auto_created=True, primary_key=True)
    profile_pic = models.ImageField(upload_to='media/profile_pic',null=True)
    phone = models.CharField(max_length=100,null=True, blank=True)
    gender = models.CharField(max_length=100,null=True, blank=True)
    bod = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=100,null=True, blank=True)
    education = models.CharField(max_length=150, null=True, blank=True)
    user_type = models.IntegerField(choices=USER,default=2)
    otp = models.IntegerField(null=True, blank=True)
    
class DeliveryAddress(models.Model):
    addressType = (
        (1,'Primary Address'),
        (1,'Secondary Address'),
    )
    delivery_address_id = models.BigAutoField(auto_created=True, primary_key=True)
    delivery_address = models.TextField(null=True)
    delivery_address_pincode = models.CharField(max_length=10,null=True)
    address_type = models.CharField(choices=addressType,max_length=50,default=1)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)
    
class Category(models.Model):
    category_id = models.BigAutoField(auto_created=True, primary_key=True)
    category_name = models.CharField(max_length=150, unique=True, null=False)
    category_img = models.ImageField(upload_to='media/category_img', null=True)

class Sub_Category(models.Model):
    subcategory_id = models.BigAutoField(auto_created=True, primary_key=True)
    subcategory_name = models.CharField(max_length=150, unique=True, null=False)
    subcategory_img = models.ImageField(upload_to='media/category_img', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

class Company(models.Model):
    company_id = models.BigAutoField(auto_created=True, primary_key=True)
    company_name = models.CharField(max_length=150, unique=True, null=False)
    company_owner_name = models.CharField(max_length=150, null=True)
    company_owner_email = models.CharField(max_length=150, unique=True, null=True)
    company_owner_phone = models.CharField(max_length=150, null=True)
    company_address = models.TextField(null=True)

class Product(models.Model):
    product_id = models.BigAutoField(auto_created=True, primary_key=True)
    product_name = models.CharField(max_length=150, unique=True, null=False)
    product_img = models.ImageField(upload_to='media/prduct_img',null=True)
    product_description = models.TextField(null=True)
    product_price = models.IntegerField(null=False)
    product_discount_price = models.IntegerField(null=True)
    product_quantity = models.IntegerField(null=False)
    product_expirydate = models.DateField(null=False)
    product_weight = models.CharField(max_length=150, null=False, blank=True)
    product_madein = models.CharField(max_length=150, null=False, blank=True)
    product_advantage = models.TextField(null=False, blank=True)
    product_disadvantage = models.TextField(null=False, blank=True)
    product_prescription_status = models.IntegerField(null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=True)

class Offer(models.Model):
    offer_id = models.BigAutoField(auto_created=True, primary_key=True)
    offer_code = models.CharField(max_length=150, unique=True, null=True)
    offer_rate = models.IntegerField(null=True)
    offer_required_amount = models.IntegerField(null=True)
    offer_description = models.TextField(null=False)
    offer_img = models.ImageField(upload_to='media/offer_img',null=True)

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Order(models.Model):
    order_id = models.BigAutoField(auto_created=True, primary_key=True)
    order_date = models.DateField(default=datetime.date.today)
    order_amount = models.CharField(max_length=20, null=False)
    order_discount_price = models.CharField(max_length=20, null=True)
    order_total_amount = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    shipping_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=10.00)
    first_name = models.CharField(max_length=30,null=True, blank=True)
    last_name = models.CharField(max_length=30,null=True, blank=True)
    email = models.CharField(max_length=50,null=True, blank=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    order_delivery_address = models.TextField(null=True, blank=True)
    order_delivery_address_pincode = models.CharField(max_length=10,null=True, blank=True)
    order_status = models.CharField(max_length=50, default="Order Confirmed")
    order_tracking_id = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=False)

    def save(self, *args, **kwargs):
        if not len(self.order_tracking_id):
            self.order_tracking_id = random_string_generator()
        super(Order,self).save(*args, **kwargs)

    @staticmethod
    def giver_order_details(order_tracking_id):
        instance = Order.objects.filter(order_tracking_id = order_tracking_id).first()
        data = {}
        data['order_tracking_id'] = instance.order_tracking_id
        data['order_total_amount'] = float(instance.order_total_amount)
        data['order_status'] = instance.order_status

        progress_status = 0
        if instance.order_status == 'Order Confirmed':
            progress_status = 20
        elif instance.order_status == 'Picked By Courier':
            progress_status = 40
        elif instance.order_status == 'On The Way':
            progress_status = 60
        elif instance.order_status == 'Ready For Pickup':
            progress_status = 80
        elif instance.order_status == 'Order Received':
            progress_status = 100
        else :
            progress_status = 0
        data['progress'] = progress_status
        return data

@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {}
        data['order_tracking_id'] = instance.order_tracking_id
        data['order_total_amount'] = float(instance.order_total_amount)
        data['order_status'] = instance.order_status

        progress_status = 0
        if instance.order_status == 'Order Confirmed':
            progress_status = 20
        elif instance.order_status == 'Picked By Courier':
            progress_status = 40
        elif instance.order_status == 'On The Way':
            progress_status = 60
        elif instance.order_status == 'Ready For Pickup':
            progress_status = 80
        elif instance.order_status == 'Order Received':
            progress_status = 100
        else : 
            progress_status = 0 
        data['progress'] = progress_status
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_tracking_id,{
                'type' : 'order_status',
                'value' : json.dumps(data)
            }
        )

class Order_Detail(models.Model):
    order_detail_id = models.BigAutoField(auto_created=True, primary_key=True)
    product_name = models.CharField(max_length=150, null=True)
    product_quantity = models.CharField(max_length=150, null=True)
    product_price = models.CharField(max_length=150, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=False)

class Cart(models.Model):
    cart_id = models.BigAutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)

class Cart_Detail(models.Model):
    cart_detail_id = models.BigAutoField(auto_created=True, primary_key=True)
    cart_quantity = models.IntegerField(null=True, default=1)
    cart_product_price = models.IntegerField(null=True)
    cart_total_price = models.IntegerField(null=True,blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    prescription_status = models.IntegerField(null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)

class Notification(models.Model):
    notification_id = models.BigAutoField(auto_created=True, primary_key=True)
    notification_message = models.TextField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=False)

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        notification_objs = Notification.objects.filter(is_seen=False).count()
        data = {'count' : notification_objs, 'current_notification' : self.notification_message}

        async_to_sync(channel_layer.group_send)(
            'new_consumer_group',{
                'type' : 'send_notification',
                'value' : json.dumps(data)
            }
        )
        super(Notification, self).save(*args,**kwargs) 

class Feedback(models.Model):
    feedback_id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    feedback_message = models.TextField(null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)

class Prescription(models.Model):
    prescription_id = models.BigAutoField(auto_created=True, primary_key=True)
    prescription_img = models.ImageField(upload_to='media/prescription_img',null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)

class Prescription_Detail(models.Model):
    prescription_detail_id = models.BigAutoField(auto_created=True, primary_key=True)
    prescription_message = models.CharField(max_length=150, null=True, blank=True)
    prescription_status = models.CharField(max_length=100, default="Pending For Approve")
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE,null=True, blank=True)
    order_detail = models.ForeignKey(Order_Detail, on_delete=models.CASCADE,null=True, blank=True)

class Payment(models.Model):
    payment_id = models.BigAutoField(auto_created=True, primary_key=True)
    payment_date = models.DateField(default=datetime.date.today)
    payment_amount = models.FloatField(null=False)
    payment_method = models.CharField(max_length=150, null=False)
    payment_status = models.CharField(max_length=150, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)