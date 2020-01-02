from rest_framework import serializers

from .models import tower


class tower_serializer(serializers.ModelSerializer): 
    class Meta:
        model = tower
        # fields = ('actual_Usage',)
        fields = '__all__'