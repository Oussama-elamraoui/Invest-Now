from rest_framework import serializers
from .models import InfoHotelsDetails
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import  Users
class InfoHotelsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoHotelsDetails
        fields = '__all__'




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Users.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                }
            }
        raise serializers.ValidationError("Invalid Credentials")

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh_token']
        return data

    def save(self, **kwargs):
        RefreshToken(self.token).blacklist()