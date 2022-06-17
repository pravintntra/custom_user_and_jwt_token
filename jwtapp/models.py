from django.db import models
from django.contrib.auth.models import AbstractUser
from jwtapp.managers import UserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your models here.
class User(AbstractUser):
    """User model"""

    username = None
    email = models.EmailField(max_length=50, unique=True)
    contact_number = models.IntegerField(null=True)
    verification = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)


class Employee(models.Model):
    name = models.CharField(max_length=50)
    roll = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class FacebookPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    posted_on = models.DateTimeField()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super(FacebookPost, self).save(*args, **kwargs)
        post = Post.objects.create(
            content_object=self,
            user=self.user,
            content=self.content,
            posted_on=self.posted_on,
        )


class TwitterPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    posted_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        super(TwitterPost, self).save(*args, **kwargs)
        post = Post.objects.create(
            content_object=self,
            user=self.user,
            content=self.content,
            posted_on=self.posted_on,
        )


class InstagramPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    posted_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        super(InstagramPost, self).save(*args, **kwargs)
        post = Post.objects.create(
            content_object=self,
            user=self.user,
            content=self.content,
            posted_on=self.posted_on,
        )


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    posted_on = models.DateTimeField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f"{self.user.id} {self.content} {self.posted_on} {self.content_type} {self.object_id} {self.content_object}"


# for proxy model understanding


class FeatureManager(models.Manager):
    def get_queryset(self):
        return super(FeatureManager, self).get_queryset().filter(type="f")


class InfographicManager(models.Manager):
    def get_queryset(self):
        return super(InfographicManager, self).get_queryset().filter(type="i")


class GalleryManager(models.Manager):
    def get_queryset(self):
        return super(GalleryManager, self).get_queryset().filter(type="g")


STORY_TYPES = (
    ("f", "Feature"),
    ("i", "Infographic"),
    ("g", "Gallery"),
)


class Story(models.Model):
    type = models.CharField(max_length=1, choices=STORY_TYPES)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    infographic = models.ImageField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "story"
        # Add verbose name
        verbose_name = "story"
        ordering = ("id",)


class FeatureStory(Story):
    objects = FeatureManager()

    class Meta:
        proxy = True


class InfographicStory(Story):
    objects = InfographicManager()

    class Meta:
        proxy = True


class GalleryStory(Story):
    objects = GalleryManager()

    class Meta:
        proxy = True


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.CharField(max_length=250)
    is_seen = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.notification

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        notification_obj = Notification.objects.filter(is_seen=False).count()
        data = {"count": notification_obj, "notification_obj": self.notification}
        async_to_sync(channel_layer.group_send)(
            "test_room_group", {"type": "send_notification", "value": json.dumps(data)}
        )
        super(Notification, self).save(*args, **kwargs)
