from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('daily-exchange-rates/', DailyRates.as_view(), name='daily_rates'),
    re_path('daily-exchange-rates/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})', DailyRatesDetails.as_view(), name='daily_rates_details'),
    path('exchange-rates/', ExchangeTypes.as_view(), name='exchange_rates'),
    re_path('exchange-rates/(?P<id>\d+)', ExchangeTypesDetails.as_view(), name='exchange_rates_details')
]