from django.db import models

from activated_mixin.models import ActivatedMixin


class ModelTest(models.Model):
    related = models.ForeignKey('SubModelTest', on_delete=models.PROTECT)


class SubModelTest(ActivatedMixin):
    identifier = models.CharField(max_length=10, default='id_test')

    def __unicode__(self):
        return '{}'.format(self.identifier)
