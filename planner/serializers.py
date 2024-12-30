from rest_framework import serializers
from .models import Expense, Settlement, PastPayment
from django.contrib.auth import get_user_model
from Travels.serializers import PhotoSerializer,TravelGroupSerializer
Users = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_name"]

class ExpenseSerializer(serializers.ModelSerializer):
    category_icon = serializers.SerializerMethodField()
    participants = serializers.CharField(required=False)
    payer = serializers.SlugRelatedField(slug_field="user_name", queryset=Users.objects.all())
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
        # Default to "Other" if no category is specified
        if not obj.category:
            category_icon = "Other.jpg"
        else:
            category_icon = obj.category_icon or "Other.jpg"  # If category_icon is not set, fallback to "Other.jpg"

        # Construct the absolute URL for the icon
        icon_path = f"/media/icons/{category_icon}"

        # Get the request object to build an absolute URL
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(icon_path)

        # Fallback URL for when no request context is available
        return f"http://triptide.pythonanywhere.com{icon_path}"
    def validate_participants(self, value):

        if isinstance(value, str):
            # Split the string by commas and strip whitespace from each username
            participants_usernames = [username.strip() for username in value.split(",") if username.strip()]
        else:
            raise serializers.ValidationError("Participants should be a comma-separated string.")

        participants = []
        for participant_username in participants_usernames:
            participant = Users.objects.filter(user_name=participant_username).first()
            if participant:
                participants.append(participant.user_id)
            else:
                raise serializers.ValidationError(f"User {participant_username} does not exist.")

        return participants
    def create(self, validated_data):
        """
        Override the create method to save participants correctly.
        """
        participants = validated_data.pop('participants', [])
        expense = Expense.objects.create(**validated_data)

        # Assign the participants to the expense
        expense.participants.set(participants)
        expense.save()

        return expense
class GetUserSerializer(serializers.ModelSerializer):
    profilePicture = serializers.SerializerMethodField("get_image")

    class Meta:
        model = Users
        fields = ["user_name","profilePicture"]

    def get_image(self, obj):
        if obj.profilePicture and hasattr(obj.profilePicture, "url"):
            return self.context["request"].build_absolute_uri(obj.profilePicture.url)
        return None


class GetExpenseSerializer(serializers.ModelSerializer):
    category_icon = serializers.SerializerMethodField()
    participants = GetUserSerializer(many=True)
    payer = GetUserSerializer()
    receipt_image = serializers.ImageField(required=False)
    travel=TravelGroupSerializer()
    class Meta:
        model = Expense
        fields = [
            "travel",
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
        if not obj.category:
            category_icon = "Other.jpg"
        else:
            category_icon = obj.category_icon or "/media/icons/Other.jpg"
        icon_path = f"{category_icon}"
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(icon_path)
        return f"http://triptide.pythonanywhere.com{icon_path}"
    def get_image(self, obj):
        if obj.receipt_image and hasattr(obj.receipt_image, "url"):
            return self.context["request"].build_absolute_uri(obj.receipt_image.url)
        return None


class PastPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastPayment
        fields = ['user', 'expense', 'amount', 'date', 'description']


class MarkAsPaidSerializer(serializers.Serializer):
    expense_id = serializers.IntegerField()
    receiver_username = serializers.CharField(max_length=100)


class MarkDebtAsPaidSerializer(serializers.Serializer):    
    payee = serializers.CharField(max_length=255)  
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    travel_name = serializers.CharField(max_length=200)

class GetPastPaySerializer(serializers.Serializer):
    receiver = GetUserSerializer()
    payer = GetUserSerializer()
    Expenses = GetExpenseSerializer()
    class Meta:
        model =PastPayment
        fields = ["Expenses", "amount", "payer", "receiver", "payment_date"]
