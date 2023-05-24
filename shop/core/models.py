from django.db import models
from jdatetime import date as jdate, datetime as jdatetime


# Create your models here.

class JalaliDateField(models.DateField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if isinstance(value, jdate):
            return value.togregorian().date()
        return value

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, jdate):
            return value.togregorian().date()
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, jdatetime):
            return value.date()
        return value


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = JalaliDateField(auto_now=True)
    is_deleted = models.BooleanField('Is Deleted', default=False, null=False, blank=False)
