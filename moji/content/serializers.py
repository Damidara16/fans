from rest_framework import serializers
#from django.contrib.auth.models import User
from django.conf import settings
from .models import *

class UserContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("__all__")

        #disabled model creation with this serializer
    def create(self,validated_data):
        return None

class CreateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        exclude = ("user","uuid","views","date")


class ContentShareRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentShareRequest
        fields = ("userTo","userFrom","content")


"""class ContentShareManageSerializer(serializers.Serializer):
    #EXPECTED ACTIONS 'ACCEPT' OR 'DENIED'
    action = serializers.CharField(max_length=6)
    uuid = UUIDSerializer()"""
