import pdb

from django.core.exceptions import ValidationError
from django.db import models

from app.utils.manager import BaseModel


def validate_minimum(value):
    if len(value) < 3:
        raise ValidationError(
            "%(value)s les than 3 character", params={"value": value},
        )


class AbstractBase(BaseModel):
    name = models.CharField(max_length=50)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name.title()

    class Meta:
        abstract = True
        ordering = ["id"]


class Country(AbstractBase):
    class Meta:
        verbose_name_plural = "countries"


class Province(AbstractBase):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="provinces")

    class Meta:
        verbose_name_plural = "provinces"


class City(AbstractBase):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities")
    code = models.CharField(
        max_length=3, null=True, blank=False, validators=[validate_minimum]
    )

    class Meta:
        verbose_name_plural = "cities"


class District(AbstractBase):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="districts")

    class Meta:
        verbose_name_plural = "districts"


class SubDistrict(AbstractBase):
    id = models.BigAutoField(primary_key=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="sub_districts")

    class Meta:
        verbose_name_plural = "sub_districts"


class Address(BaseModel):
    country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.SET_NULL, related_name="address"
    )
    province = models.ForeignKey(
        Province, null=True, blank=True, on_delete=models.SET_NULL, related_name="address"
    )
    city = models.ForeignKey(
        City, null=True, blank=True, on_delete=models.SET_NULL, related_name="address"
    )
    district = models.ForeignKey(
        District, null=True, blank=True, on_delete=models.SET_NULL, related_name="address"
    )
    sub_district = models.ForeignKey(
        SubDistrict, null=True, blank=True, on_delete=models.SET_NULL, related_name="address"
    )
    address = models.CharField(max_length=500)
    postal_code = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        # abstract = True
        ordering = ["id"]

    def __str__(self):
        return f"{self.address}, {self.postal_code if self.postal_code else ''}"

    def clean(self):
        if self.sub_district and self.district is None:
            self.district = self.sub_district.district
        elif self.sub_district.district != self.district:
            raise ValidationError("Pemilihan district dan sub district tidak sesuai.")

        if self.district and self.city is None:
            self.city = self.district.city
        elif self.district.city != self.city:
            raise ValidationError("Pemilihan city dan district tidak sesuai.")

        if self.city and self.province is None:
            self.province = self.city.province
        elif self.city.province != self.province:
            raise ValidationError("Pemilihan province dan city tidak sesuai.")

        if self.province and self.country is None:
            self.country = self.province.country
        elif self.province.country != self.country:
            raise ValidationError("Pemilihan country dan province tidak sesuai.")



