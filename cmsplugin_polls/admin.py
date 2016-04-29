from cmsplugin_polls.models import Poll, Choice
from django.contrib import admin


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 5


class PollAdmin(admin.ModelAdmin):
    model = Poll
    inlines = [ChoiceInline]


admin.site.register(Poll, PollAdmin)
