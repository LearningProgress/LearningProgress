from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import MockExamBranch, Section

admin.site.register(MockExamBranch)
admin.site.register(Section, MPTTModelAdmin)
