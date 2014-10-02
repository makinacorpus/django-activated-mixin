from django.contrib import admin

from activated_mixin.admin import GenericModelAdmin
from activated_mixin.tests.models import SubModelTest


admin.site.register(SubModelTest, GenericModelAdmin)
