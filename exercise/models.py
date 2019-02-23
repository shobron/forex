from django.db import models
from django.utils.dateparse import parse_date
from django.db.models import Avg
from datetime import timedelta


# Create your models here.
class ExchangeType(models.Model):
    origin = models.CharField(max_length=8)
    destination = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
            unique_together = (('origin', 'destination'),)

class ExchangeRate(models.Model):
    rate = models.FloatField()
    date = models.DateField()
    currency = models.ForeignKey(ExchangeType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
            unique_together = (('date', 'currency'),)

    def to_dict(self, date_input):
        weekly_average = ExchangeRate.objects.filter(
            date__lte=date_input,
            date__gt=(date_input-timedelta(days=7))
        ).aggregate(Avg('rate'))
        
        return {
            'from': self.currency.origin,
            'to': self.currency.destination,
            'rate': self.rate,
            '7-days avg': weekly_average['rate__avg']
        }
