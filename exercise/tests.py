from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from .serializers import *
from django.utils.dateparse import parse_date
import json
from collections import OrderedDict

# Create your tests here.
class ExchangeTypeModelTest(TestCase):
    def test_to_dict(self):
        date = parse_date('2019-02-22')
        self.currency = ExchangeType.objects.create(origin='IDR', destination='SGD')
        self.exchange_rate = ExchangeRate.objects.create(
            rate=0.000096, date=date, currency=self.currency       
        )
        exp_data = self.exchange_rate.to_dict(date)
        result = {
            'from': self.currency.origin,
            'to': self.currency.destination,
            'rate': self.exchange_rate.rate,
            '7-days avg': self.exchange_rate.rate
        }
        self.assertEqual(exp_data, result)

class DailyRatesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.invalid_data = {
            "date": "2018-02-22a",
            "from": "IDRrrrrrrr",
            "to": "SGD",
            "rate": "0.000096"
        }
        self.valid_data = {
            "date": "2018-02-22",
            "from": "IDR",
            "to": "SGD",
            "rate": "0.000096"
        }

    def test_post(self):
        url = reverse('daily_rates')

        # test POST with empty data
        response = self.client.post(url, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # test POST with invalid data
        response = self.client.post(url, data=json.dumps(self.invalid_data), 
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # test POST with valid data
        response = self.client.post(url, data=json.dumps(self.valid_data), 
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExchangeType.objects.count(), 1)
        self.assertEqual(ExchangeRate.objects.count(), 1)

class DailyRatesDetailsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.date = parse_date('2019-02-22')
        self.currency = ExchangeType.objects.create(origin='IDR', destination='SGD')
        self.exchange_rate = ExchangeRate.objects.create(
            rate=0.000096, date=self.date, currency=self.currency       
        )
        self.exp_data = [
            {
                'from': self.currency.origin,
                'to': self.currency.destination,
                'rate': self.exchange_rate.rate,
                '7-days avg': self.exchange_rate.rate
            }
        ]

    def test_get(self):
        # test GET with invalid data
        response = self.client.get(reverse('daily_rates_details', 
            kwargs={'year': '1234', 'month': '17', 'day': '32'}))
        self.assertEqual(response.status_code, 400)
        
        # test GET with valid data
        response = self.client.get(reverse('daily_rates_details', 
            kwargs={'year': '2019', 'month': '02', 'day': '22'}))
        self.assertEqual(response.status_code, 200)

        # result test
        self.assertEqual(response.data, self.exp_data)

class ExchangeTypesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.currency = ExchangeType.objects.create(origin='IDR', destination='SGD')
        self.exp_data = [OrderedDict([('id', self.currency.id), 
            ('from', self.currency.origin), ('to', self.currency.destination)])]
        self.invalid_data = {
            "from": "IDRrrrrrrr",
            "to": "SGDaddsda"
        }
        self.valid_data = {
            "from": "MYR",
            "to": "SGD"
        }

    def test_get(self):
        response = self.client.get(reverse('exchange_rates'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.exp_data)
        
    def test_post(self):
        url = reverse('exchange_rates')

        # test POST with empty data
        response = self.client.post(url, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # test POST with invalid data
        response = self.client.post(url, data=json.dumps(self.invalid_data), 
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # test POST with valid data
        response = self.client.post(url, data=json.dumps(self.valid_data), 
            content_type='application/json')
        self.assertEqual(response.status_code, 201)

class ExchangeTypesDetailsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.currency = ExchangeType.objects.create(origin='IDR', destination='AUD')
  
    def test_get(self):
        response = self.client.get(reverse('exchange_rates_details', 
            kwargs={'id': self.currency.id}))
        self.assertEqual(response.status_code, 200)
    
    def test_delete(self):
        response = self.client.delete(reverse('exchange_rates_details', 
            kwargs={'id': self.currency.id}))
        self.assertEqual(response.status_code, 200)





