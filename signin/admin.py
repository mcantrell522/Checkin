from models import *
from django.contrib import admin

class RecordAdmin(admin.ModelAdmin):
    fields = ['member']
    
class MemberAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname')

admin.site.register(Member, MemberAdmin)
admin.site.register(Advertisingmethod)
admin.site.register(Event)
admin.site.register(Record, RecordAdmin)
