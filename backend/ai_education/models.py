from django.db import models
from application import settings


# Create your models here.


class Question(models.Model):
    id = models.BigAutoField(
        primary_key=True, help_text="Id", verbose_name="Id")
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name='creator_query', null=True,
                                verbose_name='创建人', help_text="创建人", on_delete=models.SET_NULL,
                                db_constraint=False)
    question_uuid = models.CharField(
        max_length=255, unique=True, help_text="问题唯一标识", verbose_name="问题唯一标识")
    question = models.TextField(help_text="问题", verbose_name="问题")
    answer = models.TextField(help_text="答案", verbose_name="答案")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",
                                           verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'question'
        ordering = ['-create_datetime']
        verbose_name = '问答表'
        verbose_name_plural = verbose_name
