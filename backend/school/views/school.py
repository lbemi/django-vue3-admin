from django.shortcuts import render

from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from school.models import School, Professional


# Create your views here.

class SchoolModelSerializer(CustomModelSerializer):
    """
    获取列表时的序列化器
    """

    class Meta:
        model = School
        fields = "__all__"


class SchoolViewSet(CustomModelViewSet):
    """
    查询学校
    """
    queryset = School.objects.all()
    serializer_class = SchoolModelSerializer
    search_fields = ['name']
    pagination_class = None


class ProfessionalModelSerializer(CustomModelSerializer):
    """
    获取列表时的序列化器
    """

    class Meta:
        model = Professional
        fields = "__all__"


class ProfessionalViewSet(CustomModelViewSet):
    """
    查询专业
    """
    queryset = Professional.objects.all()
    serializer_class = ProfessionalModelSerializer
    search_fields = ['special_name']
    filter_fields = ['school_id']
    pagination_class = None
