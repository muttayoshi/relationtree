import pdb

from django.db import models
from django.contrib import admin
from django.utils import timezone


class IsDeletedManager(models.Manager):
    def get_queryset(self):
        return (
            super(IsDeletedManager, self)
            .get_queryset()
            .filter(is_deleted=False)
        )


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    date_deleted = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=254, null=True, blank=True)
    created_by = models.CharField(max_length=254, null=True, blank=True)
    updated_by = models.CharField(max_length=254, null=True, blank=True)

    objects = IsDeletedManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.date_deleted = timezone.now()
        super().save()

    class Meta:
        abstract = True
        ordering = ["id"]


class BaseAdmin(admin.ModelAdmin):
    exclude = ("is_deleted", "date_deleted", "deleted_by", "created_by", "updated_by")

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.date_deleted = timezone.now()
            obj.is_deleted = True
            obj.deleted_by = request.user.email
            obj.delete()

    def delete_model(self, request, queryset):
        queryset.date_deleted = timezone.now()
        queryset.is_deleted = True
        queryset.deleted_by = request.user.email
        queryset.delete()

    def save_model(self, request, obj, form, change):
        if obj.id:
            obj.updated_by = request.user.email
            obj.save()
        else:
            obj.created_by = request.user.email
            obj.save()
