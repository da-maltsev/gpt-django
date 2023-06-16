from django.contrib import admin

from gpt.models import OpenAiProfile
from gpt.models import Reply


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("question", "author", "status")
    list_filter = ("status", "author")
    search_fields = ("question", "answer")
    ordering = ("-created",)
    fieldsets = ((None, {"fields": ("question", "answer", "previous_reply", "author", "status")}),)
    readonly_fields = ("previous_reply",)


@admin.register(OpenAiProfile)
class OpenAiProfileAdmin(admin.ModelAdmin):
    list_display = ("uuid", "token", "usage_count", "status")
    list_filter = ("status",)
    ordering = ("-created",)
    search_fields = ("uuid", "token", "comment")
