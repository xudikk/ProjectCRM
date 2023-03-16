from django.contrib import admin

# Register your models here.

from .models.extra import *


class Students(admin.StackedInline):
    model = GroupStudent
    extra = 3


class GroupAdmin(admin.ModelAdmin):
    inlines = [Students]


admin.site.register(Member)
admin.site.register(Position)
admin.site.register(Course)
admin.site.register(Interested)
admin.site.register(Group, GroupAdmin)



