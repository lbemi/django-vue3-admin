from django.urls import path

from education.views.chat import ChatViewSet

# router = SimpleRouter()
# router.register("chat", ChatViewSet)

urlpatterns = [
    path("chat", ChatViewSet.as_view()),
]

# urlpatterns += router.urls
