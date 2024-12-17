from django.http import JsonResponse
from django.views import View
import json
from ably import AblyRest
from django.conf import settings
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def AblyMessagePublishView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        travel_name = data.get('travel_name')
        token = data.headers.get('Authorization')

        if not message or not travel_name or not token:
            return JsonResponse({"error": "Missing required parameters"}, status=400)

        user = get_user_from_token(token)
        if not user:
            return JsonResponse({"error": "Invalid or expired token"}, status=400)

        travel, tg = get_travel_and_group(travel_name, user)

        ably = AblyRest(settings.ABLY_API_KEY)
        room_group_name = f"travel_{travel_name}"
        channel = ably.channels.get(room_group_name)

        channel.publish("chat", {"message": message, "user_name": user.user_name})

        ChatMessage.objects.create(
            sender=user,
            travellers_group=tg,
            message=message,
            travel_name=travel_name,
        )

        logger.info(f"Message published to Ably channel: {room_group_name}")
        return JsonResponse({"status": "Message published successfully"}, status=200)

def get_user_from_token(token):
    try:
        import jwt
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        from django.contrib.auth import get_user_model
        user = get_user_model().objects.filter(user_id=user_id).first()
        return user
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
    return None

def get_travel_and_group(travel_name, user):
    from Travels.models import Travel, TravellersGroup

    try:
        travel = Travel.objects.get(name=travel_name)
        travellers_group = TravellersGroup.objects.prefetch_related("users").get(
            travel_is=travel
        )
        if user in travellers_group.users.all() or user == travel.admin:
            logger.info(f"Travel and travellers group found for {travel_name}.")
            return travel, travellers_group
        logger.warning(f"User {user.user_id} is not in group for travel {travel_name}.")
        return None, None
    except Travel.DoesNotExist:
        logger.warning(f"Travel {travel_name} does not exist.")
        return None, None
    except TravellersGroup.DoesNotExist:
        logger.warning(f"Travellers group for travel {travel_name} does not exist.")
        return None, None
    except Exception as e:
        logger.error(f"Error in get_travel_and_group: {e}")
        return None, None
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Real-time Chat</title>
# </head>
# <body>
#     <h1>Real-time Chat</h1>
#     <div id="messages"></div>

#     <input type="text" id="message" placeholder="Type your message here">
#     <button onclick="sendMessage()">Send</button>

#     <script src="https://cdn.ably.com/lib/ably.min.js"></script>
#     <script>
#         // Initialize Ably
#         var ably = new Ably.Realtime({ key: 'your-api-key' });

#         // Get the travel name from the URL or elsewhere (this could come from Django context)
#         var travelName = 'some_travel_name';  // Replace with actual value

#         // Create the channel for the specific travel group
#         var channel = ably.channels.get('travel_' + travelName);

#         // Subscribe to the 'chat' event to listen for incoming messages
#         channel.subscribe('chat', function(message) {
#             console.log("Received message:", message);
#             document.getElementById("messages").innerHTML += `<p>${message.data.user_name}: ${message.data.message}</p>`;
#         });

#         // Function to send a message to the server (and eventually Ably)
#         function sendMessage() {
#             var message = document.getElementById("message").value;
#             var token = 'your-jwt-token';  // You should provide the token here

#             fetch('/publish_message/', {
#                 method: 'POST',
#                 headers: {
#                     'Authorization': 'Bearer ' + token,
#                     'Content-Type': 'application/json',
#                 },
#                 body: JSON.stringify({
#                     message: message,
#                     travel_name: travelName
#                 })
#             })
#             .then(response => response.json())
#             .then(data => {
#                 console.log("Server response:", data);
#                 // Optionally, clear the input field after sending
#                 document.getElementById("message").value = '';
#             })
#             .catch(error => console.error('Error:', error));
#         }
#     </script>
# </body>
# </html>
