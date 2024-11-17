from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

User = get_user_model()

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'city', 'user_name', 'profile_picture',
            'gender', 'bio', 'email', 'password', 'current_password', 
            'new_password', 'confirm_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def validate(self, data):
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password or confirm_password:
            if not current_password:
                raise serializers.ValidationError("Current password is required to set a new password.")
            if not self.instance.check_password(current_password):
                raise serializers.ValidationError("Current password is incorrect.")
            if new_password != confirm_password:
                raise serializers.ValidationError("New password and confirm password do not match.")
            validate_password(new_password)

        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        new_password =validated_data.pop('new_password', None)
        if password:
            instance.set_password(new_password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
