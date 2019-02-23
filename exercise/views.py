from django.shortcuts import render
from django.utils import timezone
from .models import *
from rest_framework import generics, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.db.models import Max, Min
from .serializers import *


# Create your views here.
class DailyRates(APIView):
    def post(self, request):
        data = request.data
        if not data:
            return Response({'details': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['date'] = parse_date(data['date'])
        if data['date'] is None:
            return Response({'date': 'invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['origin'] = data.pop('from')
        data['destination'] = data.pop('to')
        serializer = DailyRatesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'details': 'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DailyRatesDetails(APIView):
    def get(self, request, year, month, day):
        result = []
        try:
            date_input = parse_date(year + '-' + month + '-' + day)
            exchange_rates = ExchangeRate.objects.filter(date=date_input)
        except Exception as e:
            return Response({'details': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        exchange_types = ExchangeType.objects.exclude(
            id__in=exchange_rates.values_list('currency', flat=True)
        )
        for item in exchange_rates.iterator():
            result.append(item.to_dict(date_input))
        if exchange_types:
            for item in exchange_types.iterator():
                result.append(
                    {
                        'from': item.origin,
                        'to': item.destination,
                        'rate': 'insufficient data',
                        '7-days avg': 'insufficient data'
                    }
                )
        return Response(result, status=status.HTTP_200_OK)

class ExchangeTypes(APIView):
    def get(self, request):
        currency = ExchangeType.objects.all()
        serializer = ExchangeTypeSerializers(currency, many=True)
        result = list(serializer.data)
        for item in result:
            item['from'] = item.pop('origin')
            item['to'] = item.pop('destination')
        return Response(result, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        if not data:
            return Response({'details': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        data['origin'] = data.pop('from')
        data['destination'] = data.pop('to')
        serializer = ExchangeTypeSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'details': 'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExchangeTypesDetails(APIView):
    def get(self, request, id):
        try:
            currency = ExchangeType.objects.get(id=id)
            exchange_rates = ExchangeRate.objects.filter(
                currency_id=id).order_by('-date')[:7]
        except Exception as e:
            return Response({'details': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        average_rates = exchange_rates.aggregate(Max('rate'))
        variance_rates = exchange_rates.aggregate(rate_diff=Max('rate') - Min('rate'))
        return Response(
            {
                'from': currency.origin,
                'to': currency.destination,
                'average': average_rates['rate__max'],
                'variance': variance_rates['rate_diff'],
                'exchange_rates': exchange_rates.values('date', 'rate')
            }, status=status.HTTP_200_OK
        )
    
    def delete(self, request, id):
        try:
            currency = ExchangeType.objects.get(id=id)
        except Exception as e:
            return Response({'details': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        currency.delete()
        return Response({'details': 'success'}, status=status.HTTP_200_OK)


