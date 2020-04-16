from django.contrib import admin
from .models import Note, Image, Tag

class ImageInline(admin.StackedInline):
    model = Image
    extra = 1

class NoteAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    fieldsets = [
        
        ('', {'fields': ['tags','name','desc','upload_time','owner']})
        
    ]

admin.site.register(Note, NoteAdmin)