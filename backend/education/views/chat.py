from django.http import StreamingHttpResponse
from rest_framework.views import APIView

from education.dashscope_ai.multi_chat_stream import DialogueManager


# @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
# def ChatViewSet(request):
#     print(request.user)
#     chat_manager = DialogueManager(1)
#     message = request.GET.get('message')
#     if not message:
#         return StreamingHttpResponse(chat_manager.get_history())
#     else:
#         return StreamingHttpResponse(chat_manager.chat(message))
#

#
class ChatViewSet(APIView):

    # @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def get(self, request):
        print(request.user)
        chat_manager = DialogueManager(1)
        message = request.GET.get('message')
        if not message:
            return StreamingHttpResponse(chat_manager.get_history())
        else:
            return StreamingHttpResponse(chat_manager.chat(message))
