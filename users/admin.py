from django.contrib import admin

# Register your models here.
from users.models import Module, Location, DataRecord

admin.site.register(Module)
admin.site.register(Location)
admin.site.register(DataRecord)