from django.db import models
from django.utils.translation import ugettext_lazy as _

from activated_mixin.managers import GenericManager, GenericActiveManager


class ActivatedMixin(models.Model):
    """ Mixin class providing activated fields to any model """

    # Default manager
    objects = GenericManager()
    # A manager to exclude not activated objects
    actives = GenericActiveManager()

    activated = models.BooleanField(_('Activated'), default=True)

    class Meta:
        abstract = True

    def delete(self):
        """
            Catch ProtectedError and deactivate instance instead of remove it
        """
        try:
            super(ActivatedMixin, self).delete()
        except models.deletion.ProtectedError:
            self.activated = False
            self.save()
