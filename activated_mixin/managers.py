from django.db import models


class GenericManager(models.Manager):
    """
        A bit redundant with GenericActiveManager but we can't use
        GenericActiveManager on related fields.
        ex : agency.customers.actives is invalid
        we need to do : agency.customers.objects.get_actives()
    """
    def get_actives(self):
        """ Filter inactive objects : activated=True """
        qs = self.get_queryset()
        return qs.filter(activated=True)


class GenericActiveManager(models.Manager):
    """
        A bit redundant with GenericManager but we can't use
        GenericManager as default Manager because deactivated objects
        wouldn't be shown in admin listings
    """
    def get_queryset(self):
        qs = super(GenericActiveManager, self).get_queryset()
        return qs.filter(activated=True)
