from rest_framework import serializers
from .models import Expense, Settlement, PastPayment
from django.contrib.auth import get_user_model

Users = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_name"]


class ExpenseSerializer(serializers.ModelSerializer):
    category_icon = serializers.SerializerMethodField()
    participants = serializers.CharField(required=False)
    payer = serializers.SlugRelatedField(
        slug_field="user_name", queryset=Users.objects.all()
    )
    receipt_image = serializers.ImageField(required=False)

    class Meta:
        model = Expense
        fields = [
            "amount",
            "created_at",
            "title",
            "category",
            "category_icon",
            "participants",
            "payer",
            "description",
            "receipt_image",
        ]

    def get_category_icon(self, obj):
        # Check if the category is not null or empty
        if obj.category:
            icon_path = (
                obj.category_icon or "media/icons/Other.jpg"
            )  # Default path if category_icon is null
        else:
            icon_path = "media/icons/Other.jpg"  # Default path if category is null

        # Build and return the absolute URL for the icon
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(icon_path)
        return f"http://triptide.pythonanywhere.com{icon_path}"

    def validate_participants(self, value):

        if isinstance(value, str):
            # Split the string by commas and strip whitespace from each username
            participants_usernames = [
                username.strip() for username in value.split(",") if username.strip()
            ]
        else:
            raise serializers.ValidationError(
                "Participants should be a comma-separated string."
            )

        participants = []
        for participant_username in participants_usernames:
            participant = Users.objects.filter(user_name=participant_username).first()
            if participant:
                participants.append(participant.user_id)
            else:
                raise serializers.ValidationError(
                    f"User {participant_username} does not exist."
                )

        return participants

    def create(self, validated_data):
        """
        Override the create method to save participants correctly.
        """
        participants = validated_data.pop("participants", [])
        expense = Expense.objects.create(**validated_data)

        # Assign the participants to the expense
        expense.participants.set(participants)
        expense.save()

        return expense


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_name", "profilePicture"]


class GetExpenseSerializer(serializers.ModelSerializer):
    category_icon = serializers.SerializerMethodField()
    participants = GetUserSerializer(many=True)
    payer = GetUserSerializer()
    receipt_image = serializers.ImageField(required=False)

    class Meta:
        model = Expense
        fields = [
            "amount",
            "created_at",
            "title",
            "category",
            "category_icon",
            "participants",
            "payer",
            "description",
            "receipt_image",
        ]

    def get_category_icon(self, obj):
        """Return the full URL of the category icon based on the category."""
        icon_path = obj.category_icon  # Get the relative path from the model's property
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(icon_path)
        return icon_path  # Fallback to relative path

    def get_image(self, obj):
        if obj.receipt_image and hasattr(obj.receipt_image, "url"):
            return self.context["request"].build_absolute_uri(obj.receipt_image.url)
        return None


class PastPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastPayment
        fields = ["user", "expense", "amount", "date", "description"]


class MarkAsPaidSerializer(serializers.Serializer):
    expense_id = serializers.IntegerField()
    receiver_username = serializers.CharField(max_length=100)
