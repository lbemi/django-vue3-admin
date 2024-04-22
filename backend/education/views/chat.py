from django.http import StreamingHttpResponse
from rest_framework import serializers
from rest_framework.views import APIView

from dvadmin.utils.serializers import CustomModelSerializer
from education.dashscope_ai.multi_chat_stream import DialogueManager, search_similar_questions
from school.models import Professional, School


class ChatSerializer(CustomModelSerializer):
    uuid = serializers.CharField()
    message = serializers.CharField()
    school_id = serializers.CharField()
    professional_id = serializers.CharField()

    class Meta:
        model = Professional
        fields = '__all__'


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
        serializer_class = ChatSerializer

        print(request.data)
        message = request.data.get('message')
        school_id = request.data.get('school_id')
        professional_id = request.data.get('professional_id')
        uuid = request.data.get('uuid')

        print(
            f'----{request.user.username} --- {request.user.id} -{uuid}- professional_id: {professional_id}- school_id:{school_id} - message: {message}')

        if not all([validate_input(value) for value in [school_id, professional_id]]):
            return StreamingHttpResponse("请求参数错误")
        chat_manager = DialogueManager(request.user.id, uuid)
        if not message:
            res = generate_message(school_id, professional_id)
            if not res:
                return StreamingHttpResponse("没有找到相关数据")
            assistant = get_assistant_message(res)
            print("assistant_message: ", assistant)
            if assistant == "":
                return StreamingHttpResponse("暂不支持")
            chat_manager.set_assistant(assistant)
            return StreamingHttpResponse(chat_manager.chat(res))
        else:
            return StreamingHttpResponse(chat_manager.chat(message))


def validate_input(value):
    """简单验证输入是否为空或仅包含空白字符"""
    if not value or value.isspace():
        return False
    return True


BASE_MESSAGE = '''
上面是和提问者先关的职业信息，
你是一名职业顾问兼大学职业指导老师，根据上面提供给的职位信息，请为一位寻求职业指导的人确定适切的职业选项，包含以下要素：职业概况和前景、职位要求、任职要求和技能要求、典型薪资水平和晋升路径。
基于你的研究和分析，提出关于如何获得该职业资格的建议和规划。注意回答要清晰、具体，并提供足够的细节和实例，以便读者全面了解该职业的各个方面。
请扩展到4到6个可选职业,您应该研究可用的各种选项，详细的解释不同职业所需的职业技能、加分项和就业市场趋势，并就如何获得特定领域的专业知识提出建议。
请在严格按照下面的格式提供您的回答：
职业描述：详细描述专业的前景
推荐职业：
    1. 详尽描述某人的职业选项
        - 岗位职责：xxxx
        - 任职要求：xxxx
        - 所需技能：(详细描述)
        - 加分项：xxxx
    2. 详尽描述某人的职业选项
        - 岗位职责：xxxx
        - 任职要求：xxxx
        - 所需技能：(详细描述)
        - 加分项：xxxx
总结和建议：
    1. 总结上述推荐职业所需技能的汇总
    2. 根据上述汇总给他提供几点学习建议
请注意，您的回答应该清晰、准确，并提供充足的细节来支持您的观点。同时，您还可以提供一些实际案例或建议，以加深读者对该职业的理解和认识,如果下面有提供职业数据,则按照下面职业数据进行回答,另外添加三到五个左右的职业供参考。
'''


def get_assistant_message(content):
    message = ''
    result = search_similar_questions(content, 0.5)
    if result and len(result) > 0:
        for item in result:
            message += f'{item.payload}'

    print("----->>>>>", message)
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

    print(message)
    return message


def get_professionals(school_id, professional_id):
    """
    获取专业列表
    :param school_id: 学校id
    :param professional_id: 专业id
    :return: 专业列表
    """
    try:
        professional = Professional.objects.get(school_id=school_id, id=professional_id)
        if not professional.course:
            # TODO 爬取课程数据
            pass

        return professional

    except Professional.DoesNotExist:
        return None


def get_school(school_id):
    """
    获取学校信息
    :param school_id: 学校id
    :return: 学校信息
    """
    return School.objects.get(code=school_id)
