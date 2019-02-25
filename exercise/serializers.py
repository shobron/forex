from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import *

class DailyRatesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateField()
    origin = serializers.CharField(max_length=8)
    destination = serializers.CharField(max_length=8)
    rate = serializers.CharField()

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=ExchangeRate.objects.all(),
                fields=('rate', 'date')
            )
        ]

    def create(self, validated_data):
        try:
            currency = ExchangeType.objects.get(origin=validated_data['origin'],
                destination=validated_data['destination'])
        except:
            currency = ExchangeType.objects.create(origin=validated_data['origin'],
                destination=validated_data['destination'])
        try:
            ExchangeRate.objects.create(rate=validated_data['rate'], 
                date=validated_data['date'], currency=currency)
        except Exception as e:
            error = {'detail': ",".join(e.args) if len(e.args) > 0 else 'invalid data'}
            raise serializers.ValidationError(error)
        return currency

class ExchangeTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExchangeType
        exclude = ['created_at', 'updated_at']