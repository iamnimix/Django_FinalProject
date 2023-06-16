from django.db import models
from jalali_date import date2jalali, datetime2jalali

# Create your models here.


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateField(auto_now=True)
    is_deleted = models.BooleanField('Is Deleted', default=False, null=False, blank=False)

    def get_jalali_date(self):
        return date2jalali(self.created).strftime('%Y/%m/%d')
