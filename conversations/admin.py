from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation admin """

    list_display = (
        "__str__",
        "count_messages",
        "count_participants",
    )


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message admin """

    list_display = (
        "__str__",
        "created",
    )
