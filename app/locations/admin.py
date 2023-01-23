from django.contrib import admin
from django.utils import timezone
from app.locations.models import Country, Province, City, District, SubDistrict, Address
from app.utils.manager import BaseAdmin


@admin.register(Country)
class CountryAdmin(BaseAdmin):
    search_fields = [
        "name",
    ]
    list_display = ("name", "created_by", "date_created", "updated_by", "date_updated")
    fields = ("name",)

    def get_queryset(self, request):
        qs = super(CountryAdmin, self).get_queryset(request)
        return qs.filter(is_deleted=False)


@admin.register(Province)
class ProvinceAdmin(BaseAdmin):
    search_fields = [
        "name", "country"
    ]
    list_display = ("name", "created_by", "date_created", "updated_by", "date_updated")
    fields = ("name", "country")
    autocomplete_fields = ['country']

    def get_queryset(self, request):
        qs = super(ProvinceAdmin, self).get_queryset(request)
        return qs.filter(is_deleted=False)


@admin.register(City)
class CityAdmin(BaseAdmin):
    search_fields = [
        "name", "province"
    ]
    list_display = ("name", "created_by", "date_created", "updated_by", "date_updated")
    fields = ("name", "province")
    autocomplete_fields = ['province']

    def get_queryset(self, request):
        qs = super(CityAdmin, self).get_queryset(request)
        return qs.filter(is_deleted=False)


@admin.register(District)
class DistrictAdmin(BaseAdmin):
    search_fields = [
        "name", "city"
    ]
    list_display = ("name", "created_by", "date_created", "updated_by", "date_updated")
    fields = ("name", "city")
    autocomplete_fields = ['city']

    def get_queryset(self, request):
        qs = super(DistrictAdmin, self).get_queryset(request)
        return qs.filter(is_deleted=False)


@admin.register(SubDistrict)
class SubDistrictAdmin(BaseAdmin):
    search_fields = [
        "name", "district"
    ]
    list_display = ("name", "created_by", "date_created", "updated_by", "date_updated")
    fields = ("name", "district")
    autocomplete_fields = ['district']

    def get_queryset(self, request):
        qs = super(SubDistrictAdmin, self).get_queryset(request)
        return qs.filter(is_deleted=False)


# admin.site.register(Address)
@admin.register(Address)
class AddressAdmin(BaseAdmin):
    search_fields = [
        "address",
    ]
    list_display = ("address", "created_by", "date_created", "updated_by", "date_updated")
    fieldsets = (
        (None, {
            "fields": (
                "address",
                "postal_code"
            )
        }),
        ("Locations", {
            "classes": ("collapse",),
            "fields": (
                "sub_district",
                "district",
                "city",
                "province",
                "country",
            ),
        }),
    )
    autocomplete_fields = [
        "sub_district",
        "district",
        "city",
        "province",
        "country",
    ]

    def get_queryset(self, request):
        qs = super(AddressAdmin, self).get_queryset(request)
        return qs.filter(is_deleted=False)
