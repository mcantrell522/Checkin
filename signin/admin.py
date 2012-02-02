from models import *
from django.contrib import admin

class RecordAdmin(admin.ModelAdmin):
    fields = ['member']

admin.site.register(Member)
admin.site.register(Advertisingmethod)
admin.site.register(Event)
admin.site.register(Record, RecordAdmin)
