from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'city', 'user_name', 'profile_picture',
            'gender', 'bio', 'email', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }



    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
