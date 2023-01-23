from django.db import models
from django.urls import reverse

from app.utils.manager import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=3)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'countries'


class Location(BaseModel):
    """A location is not meant to be a pinpoint address but a general place such
    as a town or village."""
    name = models.CharField(max_length=50, help_text='Place name')
    county_state_province = models.CharField(max_length=30,
                                             verbose_name='county/state/province',
                                             help_text='County / state / province')
    country = models.ForeignKey(Country, models.CASCADE, help_text='Country')
    # If left blank, these fields will be set by geocoding when the model is saved.
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # if not (self.latitude and self.longitude):
        #     try:
        #         geocoder = OpenCageGeocode(settings.OPENCAGE_API_KEY)
        #         query = '{0}, {1}, {2}'.format(self.name,
        #                                        self.county_state_province,
        #                                        self.country.name)
        #         result = geocoder.geocode(query)
        #         geometry = result[0].get('geometry')
        #         self.latitude = geometry.get('lat')
        #         self.longitude = geometry.get('lng')
        #     except Exception as e:
        #         # If something goes wrong, there's not much we can do, just leave
        #         # the coordinates blank.
        #         print(e)
        super(Location, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('location', args=[self.id])

    def __str__(self):
        return '{0}, {1}'.format(self.name, self.county_state_province)

    def __eq__(self, other):
        if other:
            return self.name == other.name and self.latitude == other.latitude and self.longitude == other.longitude
        else:
            return False

    def __hash__(self):
        return hash(self.name) + hash(self.latitude) + hash(self.longitude)

    class Meta:
        ordering = ['country', 'county_state_province', 'name']
        unique_together = [('country', 'county_state_province', 'name')]