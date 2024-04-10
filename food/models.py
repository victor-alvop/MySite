from django.db import models

# Create your models here.
class item(models.Model):

    def __str__(self):
        return self.item_name

    item_name = models.CharField(max_length=200)
    item_description = models.CharField(max_length=500)
    item_price = models.IntegerField()
    item_image = models.CharField(max_length=700, default = 'https://theme-assets.getbento.com/sensei/5271791.sensei/assets/images/catering-item-placeholder-704x520.png' )