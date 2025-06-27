from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import LabModule

@admin.register(LabModule)
class LabModuleAdmin(admin.ModelAdmin):
    list_display = ('lab_name', 'container_name', 'tier')
    search_fields = ('lab_name', 'container_name')
    list_filter = ('tier',)
