from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import re
from django.contrib.auth import get_user_model
User = get_user_model()


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    currentPassword = serializers.CharField(required=True, write_only=True)
    newPassword = serializers.CharField(required=False, write_only=True)
    # confirmPassword = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'firstName', 'lastName', 'city', 'user_name', 'profilePicture','currentPassword', 'newPassword',
            'gender', 'bio', 'email', 'phone', 'birthDate'
        ]


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
        currentPassword = data.get('currentPassword')
        newPassword = data.get('newPassword')

        if newPassword:
            if 'confirmPassword' in data and data.get('confirmPassword') != newPassword:
                raise serializers.ValidationError("New password and confirm password must match.")

            # Ensure current password is correct
        if currentPassword:
            user = self.context['request'].user
            if not user.check_password(currentPassword):
                raise serializers.ValidationError("Current password is incorrect.")

        return data
    def get_profilePicture(self, obj):
        if obj.profilePicture:
            return obj.profilePicture.url
        return None  # You could return a default image URL if desired

    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError("The email must contain '@'.")
        return value

    def update(self, instance, validated_data):
        currentPassword = validated_data.pop('currentPassword', None)
        newPassword = validated_data.pop('newPassword', None)

        # Check if currentPassword is correct and change to new password
        if currentPassword:
            if not instance.check_password(currentPassword):
                raise serializers.ValidationError("Current password is incorrect.")
            if newPassword:
                instance.set_password(newPassword)

        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

