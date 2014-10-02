from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


def highlight_deactivated(obj):
    """
        Display in red lines where object is deactivated (i.e. activated=False)
    """
    if getattr(obj, 'activated', True):
        return obj
    else:
        return '<em style="color:#ff3e3e; font-weight:normal">{}</em>'\
            .format(obj)
highlight_deactivated.short_description = _("Name")
highlight_deactivated.allow_tags = True


class GenericModelAdmin(admin.ModelAdmin):
    """ Generic admin model with common configuration like:
        - filter on 'activated'
        - highlight inactive objects
    """
    list_filter = ('activated',)
    list_display = (highlight_deactivated,)
    search_fields = ['name']
