from django.contrib import admin
from .models import Member, Schedule, BlogPost, CheckIn

# Register your models here
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'membership_id', 'status', 'created_at')
    search_fields = ('name', 'membership_id')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'start_time', 'end_time')
    search_fields = ('title', 'instructor')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    search_fields = ('title',)

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('member', 'timestamp', 'synced')
    search_fields = ('member__name',)
