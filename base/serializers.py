# base/serializers.py
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re
import phonenumbers

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'username','email','password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},  # Enforce required
            'phone_number': {'required': True},
            'username': {'required': True}
        }
    def validate_phone_number(self, value):
        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(value, None)
            
            # Check if the phone number is valid
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError(
                    "Invalid phone number. Please provide a valid phone number with country code (e.g., +919689196091)."
                )
            
            # Ensure it has a country code
            if not value.startswith('+'):
                raise serializers.ValidationError(
                    "Phone number must include a country code starting with '+' (e.g., +919689196091)."
                )
            
            # Format to E.164 and check length
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            if len(formatted_number) > 15:
                raise serializers.ValidationError(
                    "Phone number must not exceed 15 characters."
                )
            
            return formatted_number  # Return standardized E.164 format
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError(
                "Unable to parse phone number. Please provide a valid phone number with country code (e.g., +919689196091)."
            )
        
    # def validate_phone_number(self, value):
    #     # Regex: Starts with +, followed by 1-3 digit country code, then 10 digits
    #     pattern = r'^\+\d{1,3}\d{10}$'
    #     if not re.match(pattern, value):
    #         raise serializers.ValidationError(
    #             "Phone number must be in the format +<country_code><10-digit-number> (e.g., +919689196091)."
    #         )
    #     if len(value) > 15:  # Respect max_length from model
    #         raise serializers.ValidationError("Phone number must not exceed 15 characters.")
    #     return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
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