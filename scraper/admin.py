from django.contrib import admin
from models import Hardware, Computer

class HardwareAdmin(admin.ModelAdmin):
	list_display = ('name', 'brand', 'certified', 'id')
	search_fields = ['name']

class ComputerAdmin(admin.ModelAdmin):
	list_display = ('name', 'brand', 'certified', 'version', 'id')
	search_fields = ['name']
	list_filter = ['version', 'certified']

admin.site.register(Hardware, HardwareAdmin)
admin.site.register(Computer, ComputerAdmin)