from django.db import models
from jdatetime import date as jdate, datetime as jdatetime
import jdatetime

# Create your models here.


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateField(auto_now=True)
    is_deleted = models.BooleanField('Is Deleted', default=False, null=False, blank=False)

    def save(self, *args, **kwargs):
        if self.created:
            j_date = jdatetime.date.fromgregorian(date=self.created)
            self.my_jalali_date = j_date.todatetime().date()
        super(BaseModel, self).save(*args, **kwargs)
