from django.contrib import admin
from app.peoples.models import Person, Marriage, Document, Photograph
from app.utils.manager import BaseAdmin


@admin.register(Person)
class PersonAdmin(BaseAdmin):
    search_fields = [
        "full_name",
    ]
    list_display = ("name", "created_by", "date_created", "updated_by", "date_updated")
    fieldsets = (
        (None, {
            "fields": (
                "full_name",
                "surname",
                "nickname",
            )
        }),
        ("Event", {
            "classes": ("collapse",),
            "fields": (
                "date_of_birth",
                "birth_location",
                "date_of_death",
            )
        }),
        ("Information", {
            "classes": ("collapse",),
            "fields": (
                "parent",
                "gender",
                "phone",
                "address",
                "notes",
                "deceased",
                "user",
            )
        }),
    )
    autocomplete_fields = [
        "birth_location",
        "parent",
        "address",
    ]

    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        return qs.filter(is_deleted=False)


@admin.register(Marriage)
class MarriageAdmin(BaseAdmin):
    search_fields = [
        "husband",
        "wife",
    ]
    list_display = ("__str__", "created_by", "date_created", "updated_by", "date_updated")
    fields = ("husband", "wife", "date", "location", "divorced", "reference",)
    autocomplete_fields = [
        "husband",
        "wife",
        "location"
    ]

    def get_queryset(self, request):
        qs = super(MarriageAdmin, self).get_queryset(request)
        return qs.filter(is_deleted=False)


@admin.register(Document)
class DocumentAdmin(BaseAdmin):
    list_display = ("title", "created_by", "date_created", "updated_by", "date_updated")

    def get_queryset(self, request):
        qs = super(DocumentAdmin, self).get_queryset(request)
        return qs.filter(is_deleted=False)


@admin.register(Photograph)
class PhotographAdmin(BaseAdmin):
    list_display = ("caption", "created_by", "date_created", "updated_by", "date_updated")

    def get_queryset(self, request):
        qs = super(PhotographAdmin, self).get_queryset(request)
        return qs.filter(is_deleted=False)
