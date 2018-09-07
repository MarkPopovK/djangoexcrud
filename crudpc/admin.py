from django.contrib import admin
from .models import Computer, Processor, RAM, Disk

admin.site.register(Computer)
admin.site.register(Processor)
admin.site.register(RAM)
admin.site.register(Disk)
