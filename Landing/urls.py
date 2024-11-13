from django.urls import path
from .views import landing_page
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("home/",landing_page),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)