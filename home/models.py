from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from organization.models import *

# Create your models here.
class categ(models.Model):
    name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(categ, self).save(*args, **kwargs)
    def __str__(self):
        return '{}'.format(self.name)
    def get_url(self):
        return reverse('prod_cat',args=[self.slug])

class products(models.Model):
    name=models.CharField(max_length=150,unique=True)
    slug =models.SlugField(max_length=250,unique=True)
    img=models.ImageField(upload_to='product')
    desc=models.TextField()
    stock=models.IntegerField()
    available=models.BooleanField()
    price=models.IntegerField()
    category=models.ForeignKey(categ,on_delete=models.CASCADE)
    date=models.DateTimeField()
    org_id=models.ForeignKey(Organization,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(products, self).save(*args, **kwargs)
    def __str__(self):
        return '{}'.format(self.name)
    class Meta:
        ordering = ['-date']
    def get_url(self):
        return reverse('detail',args=[self.category.slug,self.slug])

