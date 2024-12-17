from django.db import models
from django.utils import timezone
from Travels.models import Travel, TravellersGroup
from django.conf import settings


class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    travellers_group = models.ForeignKey(TravellersGroup, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    travel_name = models.CharField(max_length=200,blank=True, null=True)
    # is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} in group {self.travellers_group} at {self.timestamp}"
