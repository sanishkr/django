from .models import IGuser, mkimg
from rest_framework import serializers


class IGUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGuser
        fields = ('username', 'password')

class MKImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = mkimg
        fields = ('ImageURL', 'Xpos', 'Ypos', 'Height', 'Width', 'Rotation')