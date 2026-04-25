from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "featured", "created_at", "updated_at")
    list_filter = ("category", "featured", "created_at")
    search_fields = ("title", "subtitle", "excerpt", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}


admin.site.site_header = "Signal & Craft Admin"
admin.site.site_title = "Signal & Craft"
admin.site.index_title = "Editorial control"
