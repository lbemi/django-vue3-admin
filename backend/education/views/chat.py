from django.http import StreamingHttpResponse
from rest_framework.views import APIView

from education.dashscope_ai.embedding import generate_embeddings
from education.dashscope_ai.multi_chat_stream import DialogueManager, search_similar_questions
from school.models import Professional, School


class ChatViewSet(APIView):
    """
      处理POST请求，与对话管理器交互以产生响应。

      参数:
      - self: 表示类的实例。
      - request: 包含请求信息的对象，来自客户端的POST请求。

      返回值:
      - StreamingHttpResponse对象，包含从对话管理器获取的响应或错误信息。
      """

    def post(self, request):
        # print(request.user)
        username = request.user
        message = request.POST.get('message')
        school_id = request.POST.get('school_id')
        professional_id = request.POST.get('professional_id')
        uuid = request.POST.get('uuid')
        chat_manager = DialogueManager(username, uuid)

        print(f'{username}-{uuid}-{}')
        if message:
            message = get_assistant_message(message)
            assistant_message = get_assistant_message(message)
            if assistant_message:
                chat_manager.set_assistant(assistant_message)
            else:
                return StreamingHttpResponse("抱歉，我无法回答你的问题")

        if not school_id or not professional_id:
            return StreamingHttpResponse("请求参数错误")
        else:
            return StreamingHttpResponse(chat_manager.chat(message))


def get_assistant_message(message):
    vec = generate_embeddings(message)
    message = None
    if vec:
        result = search_similar_questions(vec)
        if result and len(result) > 0:
            for item in result:
                if item.score > 0.8:
                    message += f"{item.content}"
        else:
            return message

        if not message:
            return message
    else:
        return message


def generate_message(school_id, professional_id):
    """
    生成消息
    :param school_id: 学校id
    :param professional_id: 专业id
    :return: 消息
    """
    professional = get_professionals(school_id, professional_id)
    school = get_school(school_id)
    message = (f'我的学校及专业信息如下：'
               f'学校：{school.name}'
               f'专业：{professional.special_name}'
               f'是否是211：{school.f211}'
               f'是否是985：{school.f985}'
               f'是否是双一流：{school.dual_class}'
               f'课程介绍：{professional.course}')

    return message


def get_professionals(school_id, professional_id):
    """
    获取专业列表
    :param school_id: 学校id
    :param professional_id: 专业id
    :return: 专业列表
    """
    professional = Professional.objects.filter(school_id=school_id, id=professional_id)
    if not professional.course:
        # TODO 爬取课程数据
        pass

    return professional


def get_school(school_id):
    """
    获取学校信息
    :param school_id: 学校id
    :return: 学校信息
    """
    return School.objects.filter(code=school_id)
