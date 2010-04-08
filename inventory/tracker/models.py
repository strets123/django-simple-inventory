from datetime import date

from django.db import models


class Product(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)
    cost_price = models.FloatField(null=True, blank=True)
    sell_price = models.FloatField(null=True, blank=True)
    qty = models.PositiveIntegerField(default=0)

    def update_qty(self, qty):
        """ creates a movement with the diff """
        mov, _ = Movement.objects.get_or_create(product=self, day=date.today())
        mov.qty += qty - self.qty
        mov.save()
        self.qty = qty
        self.save()

    def qty_on(self, day):
        """ returns qty on specific day """
        return self.qty - sum(
            Movement.objects.filter(product=self, day__range=(day,
                date.today())).values_list('qty', flat=True))


class Movement(models.Model):
    product = models.ForeignKey(Product)
    day = models.DateField(default=date.today())
    qty = models.IntegerField(default=0)

    class Meta:
        unique_together = ('product', 'day')
