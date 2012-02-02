from sec.signin.models import *
from django.contrib import admin

class RecordAdmin(admin.ModelAdmin):
    fields = ['member']

admin.site.register(Member)
admin.site.register(Society)
admin.site.register(GAM)
admin.site.register(Record, RecordAdmin)
