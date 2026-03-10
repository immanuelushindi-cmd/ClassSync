from django.contrib import admin
from .models import Session, Doubt, Vote


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display  = ('title', 'subject', 'pin', 'teacher_name', 'is_active', 'created_at')
    list_filter   = ('is_active', 'subject')
    search_fields = ('title', 'teacher_name', 'pin')
    readonly_fields = ('pin', 'created_at')


@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    list_display  = ('text_short', 'session', 'topic_tag', 'votes', 'is_answered', 'submitted_at')
    list_filter   = ('is_answered', 'session')
    search_fields = ('text', 'topic_tag')

    def text_short(self, obj):
        return obj.text[:60]
    text_short.short_description = 'Doubt'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('doubt', 'voter_key')
