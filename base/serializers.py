# base/serializers.py
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'username', 'password']

    def validate_phone_number(self, value):
        # Regex: Starts with +, followed by 1-3 digit country code, then 10 digits
        pattern = r'^\+\d{1,3}\d{10}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Phone number must be in the format +<country_code><10-digit-number> (e.g., +919689196091)."
            )
        if len(value) > 15:  # Respect max_length from model
            raise serializers.ValidationError("Phone number must not exceed 15 characters.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            phone_number=validated_data['phone_number'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        credentials = {
            'phone_number': attrs.get('phone_number'),
            'password': attrs.get('password')
        }

        if not credentials['phone_number'] or not credentials['password']:
            raise serializers.ValidationError('Must include "phone_number" and "password".')

        user = CustomUser.objects.filter(phone_number=credentials['phone_number']).first()
        if user and user.check_password(credentials['password']):
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            data = super().validate(attrs)
            data['username'] = user.username
            return data
        else:
            raise serializers.ValidationError('Unable to log in with provided credentials.')