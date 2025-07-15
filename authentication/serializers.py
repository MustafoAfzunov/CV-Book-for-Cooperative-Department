from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_pending']
        extra_kwargs = {'password': {'write_only': True}, 'is_pending': {'read_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_pending=True  
        )
        return user

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("No user with this email exists.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        print("Validating data:", data)
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError({"non_field_errors": ["Invalid user ID."]})

        if not PasswordResetTokenGenerator().check_token(user, data['token']):
            raise serializers.ValidationError({"non_field_errors": ["Invalid or expired token."]})

        if len(data['new_password']) < 8:
            raise serializers.ValidationError({"new_password": ["Password must be at least 8 characters."]})
        data['user'] = user
        return data

    def save(self):
        password = self.validated_data['new_password']
        user = self.validated_data['user']
        user.set_password(password)
        user.save()
        return user