from rest_framework import serializers
from django.contrib.auth.models import User

from .models import contact
class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class contactSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField(source = 'User', read_only = True)
    class Meta:
        model = contact
        fields = '__all__'

    def create(self, validated_data):
        return contact.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.firstName = validated_data.get('firstName')
        instance.lastName = validated_data.get('lastName')
        instance.number = validated_data.get('number')
        instance.note = validated_data.get('note')
        instance.address = validated_data.get('address')
        instance.birthDate = validated_data.get('birthDate')
        instance.save()
        return instance