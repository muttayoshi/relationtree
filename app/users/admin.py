from django.contrib import admin
from app.users.models import Person, Event, Marriage, Photograph, Document, SurnameVariant


admin.site.register(Person)
admin.site.register(Event)
admin.site.register(Marriage)
admin.site.register(Photograph)
admin.site.register(Document)
admin.site.register(SurnameVariant)
