from django.contrib import admin
from jwtapp.models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

# Register your models here.


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "notification", "is_seen", "created_on"]
    list_filter = (
        "is_seen",
        "created_on",
    )
    search_fields = ("notification",)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ["id", "type", "title", "body", "infographic", "link"]
    list_filter = ("type",)
    search_fields = (
        "title",
        "body",
    )
    fields = (
        "title",
        "body",
        "type",
        "link",
        "infographic",
    )

    def make_change_type(modeladmin, request, queryset):
        queryset.update(type="g")
        messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True

    admin.site.add_action(make_change_type, "Story type Change")


admin.site.register(Employee)
admin.site.register(ContentType)
admin.site.register(FacebookPost)
admin.site.register(TwitterPost)
admin.site.register(InstagramPost)
admin.site.register(Post)
admin.site.register(FeatureStory)
admin.site.register(InfographicStory)
admin.site.register(GalleryStory)
