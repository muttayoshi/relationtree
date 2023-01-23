from django.contrib import admin
from app.locations.models import Country, Province, City, District, SubDistrict, Address


admin.site.register(Country)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(District)
admin.site.register(SubDistrict)
admin.site.register(Address)
