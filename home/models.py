from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class Category(models.Model):
    sub_category = models.ForeignKey('self', related_name='sub', on_delete=models.CASCADE ,null=True , blank=True)
    sub_cat = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True, unique=True , blank=True , null=True )
    image = models.ImageField(upload_to='Category' , null=True , blank=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('home:category' , args=[self.slug , self.id])
class Product(models.Model):
    VARIANT =(
        ('None' , 'none'),
        ('Size' , 'size'),
        ('Color' , 'color'),
    )
    category = models.ManyToManyField(Category, blank=True)
    name = models.CharField(max_length=150)
    amount = models.PositiveSmallIntegerField()
    unit_price = models.IntegerField()
    discount = models.PositiveSmallIntegerField(null=True , blank=True)
    total_price = models.PositiveIntegerField()
    information = models.TextField(null=True , blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(null=True , choices=VARIANT , blank=True , max_length=20)
    tags = TaggableManager(blank=True)
    image = models.ImageField(upload_to='Product')
    like = models.ManyToManyField(User, blank=True , related_name='product_like')
    unlike = models.ManyToManyField(User, blank=True , related_name='product_unlike')
    total_like = models.PositiveSmallIntegerField(default=0)
    total_unlike = models.PositiveSmallIntegerField(default=0)

    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount *self.unit_price) / 100
            return  int(self.unit_price - total)
        return self.total_price


class Size(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Variants(models.Model):
    name = models.CharField(max_length=150)
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(Size, on_delete=models.CASCADE , null=True , blank=True)
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveSmallIntegerField()
    unit_price = models.IntegerField()
    discount = models.PositiveSmallIntegerField(null=True , blank=True)
    total_price = models.PositiveIntegerField()
    def __str__(self):
        return self.name


class Comment(models.Model):
        post = models.ForeignKey(Product, on_delete=models.CASCADE)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        content = models.TextField(max_length=160)
        timestamp = models.DateTimeField(auto_now_add=True)
        def __str__(self):
            return self.content