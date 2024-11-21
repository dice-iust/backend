from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
# from signup.models import UserProfile

User = get_user_model()
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    currentPassword = serializers.CharField(
        required=False,
        write_only=False,
        help_text="Enter your current password to validate the change."
    )
    newPassword = serializers.CharField(
        required=False,
        write_only=False,
        help_text="Enter your new password."
    )
    confirmPassword = serializers.CharField(
        required=False,
        write_only=False,
        help_text="Re-enter your new password to confirm it."
    )

    class Meta:
        model = User
        fields = [
            'firstName', 'lastName', 'city', 'user_name', 'profilePicture',
            'gender', 'bio', 'email', 'phone', 'birthDate', 'password',
            'currentPassword', 'newPassword', 'confirmPassword'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def validate(self, data):
        currentPassword = data.get('currentPassword')
        newPassword = data.get('newPassword')
        confirmPassword = data.get('confirmPassword')

        if newPassword or confirmPassword:
            if not currentPassword:
                raise serializers.ValidationError("Current password is required to set a new password.")
            if not self.instance.check_password(currentPassword):
                raise serializers.ValidationError("Current password is incorrect.")
            if newPassword != confirmPassword:
                raise serializers.ValidationError("New password and confirm password do not match.")
            validate_password(newPassword)

        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        newPassword = validated_data.pop('newPassword', None)

        if newPassword:
            instance.set_password(newPassword)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
