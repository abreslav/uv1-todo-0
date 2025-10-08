from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'marked_as_done_at', 'is_done')
    list_filter = ('created_at', 'marked_as_done_at')
    search_fields = ('content',)
    readonly_fields = ('created_at',)

    def is_done(self, obj):
        return obj.is_done
    is_done.boolean = True
    is_done.short_description = 'Completed'
