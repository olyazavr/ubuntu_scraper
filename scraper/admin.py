from django.contrib import admin
from models import Hardware, Computer, Processor

class HardwareAdmin(admin.ModelAdmin):
	list_display = ('name', 'brand', 'certified', 'id', 'source')
	search_fields = ['name']
	list_filter = ['source']

class ComputerAdmin(admin.ModelAdmin):
	list_display = ('name', 'brand', 'certified', 'version', 'id', 'source')
	search_fields = ['name']
	list_filter = ['version', 'certified', 'source']

class ProcessorAdmin(admin.ModelAdmin):
	list_display = ('name', 'codename', 'graphics', 'id', 'source')
	search_fields = ['name', 'codename', 'graphics']
	list_filter = ['codename', 'graphics', 'source']

admin.site.register(Hardware, HardwareAdmin)
admin.site.register(Computer, ComputerAdmin)
admin.site.register(Processor, ProcessorAdmin)