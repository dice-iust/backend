from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import re
from django.contrib.auth import get_user_model
User = get_user_model()

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'firstName', 'lastName', 'city', 'user_name', 'profilePicture',
            'gender', 'bio', 'email', 'phone', 'birthDate', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError("The email must contain '@'.")
        return value

    def validate_password(self, value):
        if value:
            if len(value) < 6:
                raise serializers.ValidationError("Password must be at least 6 characters long.")
            if not re.search(r'[A-Za-z]', value):
                raise serializers.ValidationError("Password must contain at least one letter.")
            if not re.search(r'\d', value):
                raise serializers.ValidationError("Password must contain at least one number.")
            if value.isdigit() or value.isalpha():
                raise serializers.ValidationError("Password cannot be all letters or all numbers.")
        return value

    def validate(self, data):
        password = data.get('password')
        if password:
            self.validate_password(password)
        return data



    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
