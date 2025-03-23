from django.contrib import admin
from .models import *

# Register your models here.
class SaveVocabAdmin(admin.ModelAdmin):
    list_display = ('word', 'definition', 'save_date', 'checked')
    list_filter = ('save_date', 'checked')
    search_fields = ('word', 'definition')
    ordering = ('save_date',)

admin.site.register(SaveVocab, SaveVocabAdmin)