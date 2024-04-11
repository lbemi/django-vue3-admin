# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class School(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255, blank=True, null=True)
    f985 = models.CharField(max_length=255, blank=True, null=True)
    f211 = models.CharField(max_length=255, blank=True, null=True)
    p = models.CharField(max_length=255, blank=True, null=True)
    c = models.CharField(max_length=255, blank=True, null=True)
    qj = models.CharField(max_length=255, blank=True, null=True)
    answer_url = models.CharField(max_length=255, blank=True, null=True)
    dual_class = models.CharField(max_length=255, blank=True, null=True)
    nature = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'school'


class Jobs(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    requirement = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    professional = models.CharField(max_length=255, blank=True, null=True)
    is_embedding = models.IntegerField(blank=True, null=True, db_comment='1: 是; 2 否')

    class Meta:
        managed = False
        db_table = 'jobs'


class Professional(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    school_id = models.CharField(max_length=10)
    special_id = models.CharField(max_length=10, blank=True, null=True)
    nation_feature = models.CharField(max_length=255, blank=True, null=True)
    province_feature = models.CharField(max_length=255, blank=True, null=True)
    is_important = models.CharField(max_length=255, blank=True, null=True)
    limit_year = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    level3_weight = models.CharField(max_length=2, blank=True, null=True)
    nation_first_class = models.CharField(max_length=255, blank=True, null=True)
    xueke_rank_score = models.CharField(max_length=255, blank=True, null=True)
    is_video = models.IntegerField(blank=True, null=True)
    special_name = models.CharField(max_length=255, blank=True, null=True)
    special_type = models.CharField(max_length=255, blank=True, null=True)
    type_name = models.CharField(max_length=255, blank=True, null=True)
    level3_name = models.CharField(max_length=255, blank=True, null=True)
    level3_code = models.CharField(max_length=255, blank=True, null=True)
    level2_name = models.CharField(max_length=255, blank=True, null=True)
    level2_id = models.CharField(max_length=8, blank=True, null=True)
    level2_code = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    course = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'professional'
