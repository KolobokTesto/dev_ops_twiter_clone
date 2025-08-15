from django.contrib import admin
from .models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'created_at', 'has_image')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username')
    readonly_fields = ('created_at',)

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image' 