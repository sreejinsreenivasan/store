from django.db import models

# Create your models here.


class Product(models.Model):
    item_code = models.CharField(max_length=50)
    item_name = models.CharField(max_length=50)
    category_l1 = models.CharField(max_length=50)
    category_l2 = models.CharField(max_length=50)
    upc = models.CharField(max_length=50)
    parent_code = models.CharField(max_length=50, null=True)
    price = models.FloatField(default=0.00)
    size = models.CharField(max_length=4)
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_children(self, parent):
        return self.objects.filter(parent_code=parent)