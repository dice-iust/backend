from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile
# from django.contrib.auth.hashers import check_password

User = get_user_model()
class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['email','user_name','password']


class UserProfileSerializer(serializers.ModelSerializer):
    user=Userserializer()
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user', 'first_name', 'last_name', 
            'city', 'gender', 'birth_date', 'profile_picture',
            'current_password', 'new_password', 'confirm_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
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
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.city = validated_data.get('city', instance.city)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)

        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data['profile_picture']

        if validated_data.get('new_password'):
            instance.set_password(validated_data['new_password'])

        instance.save()
        return instance
