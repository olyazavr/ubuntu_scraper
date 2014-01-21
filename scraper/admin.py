from django.contrib import admin
from models import Hardware, Computer

class HardwareAdmin(admin.ModelAdmin):
	list_display = ('name', 'brand', 'certified', 'id', 'source')
	search_fields = ['name']
	list_filter = ['source']

class ComputerAdmin(admin.ModelAdmin):
	list_display = ('name', 'brand', 'certified', 'version', 'id', 'source')
	search_fields = ['name']
	list_filter = ['version', 'certified', 'source']

admin.site.register(Hardware, HardwareAdmin)
admin.site.register(Computer, ComputerAdmin)