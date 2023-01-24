import os
from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from tinymce.models import HTMLField

from app.utils.fields import UncertainDateField
from app.utils.manager import BaseModel


class Person(BaseModel):
    full_name = models.CharField(max_length=60, help_text='Nama Lengkap')
    surname = models.CharField(max_length=30, help_text='Nama Keluarga')
    nickname = models.CharField(max_length=30, help_text='Nama Panggilan')
    gender = models.CharField(
        max_length=1,
        choices=(('M', 'Male'), ('F', 'Female')),
        blank=False,
        default=None
    )
    date_of_birth = UncertainDateField(help_text="YYYY-MM-DD", blank=True, null=True)
    birth_location = models.ForeignKey(
        "locations.City",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name="Tempat Lahir",
    )
    address = models.ForeignKey(
        "locations.Address",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name="Tempat Tinggal",
    )
    phone = models.CharField(max_length=15, null=True, blank=True, help_text="6281234567890")
    date_of_death = UncertainDateField(help_text="YYYY-MM-DD", blank=True, null=True)
    deceased = models.BooleanField(default=False, help_text="Alm")
    parent = models.ForeignKey(
        "Marriage",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )
    notes = HTMLField(blank=True, null=True)
    user = models.OneToOneField(User, models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['surname', '-date_of_birth']

    def name(self, use_surname=False, use_nickname=False):
        name = self.full_name.title()
        if use_surname and self.surname:
            name = f"{name} {self.surname.title()}"
        if use_nickname and self.nickname:
            name = f"{name} ({self.nickname})"
        return name

    def age(self):
        """Calculate the person's age in years."""
        if not self.date_of_birth or (self.deceased and not self.date_of_death):
            return None
        end = self.date_of_death if self.deceased else date.today()
        years = end.year - self.date_of_birth.year
        if end.month and self.date_of_birth.month:
            if (
                    end.month < self.date_of_birth.month or
                    (
                        end.month == self.date_of_birth.month
                        and end.day
                        and self.date_of_birth.day
                        and end.day < self.date_of_birth.day
                    )
            ):
                years -= 1
        return years

    def is_age_exact(self):
        """If the date of birth and/or date of death isn't known precisely then
        the age might be off by up to a year."""
        if self.date_of_birth is None or self.date_of_birth.is_uncertain():
            return False
        if self.deceased and (self.date_of_death is None or self.date_of_death.is_uncertain()):
            return False
        return True

    def whatsapp(self):
        if self.phone is None:
            return None
        else:
            return f"https://wa.me/{self.phone}"

    def spouses(self):
        """Return a list of anybody that this person is or was married to."""
        if self.gender == 'F':
            return [(m.husband, m.date, m.location, m.divorced) for m in self.wife_of.order_by('date').all()]
        else:
            return [(m.wife, m.date, m.location, m.divorced) for m in self.husband_of.order_by('date').all()]

    def full_siblings(self):
        """Returns a list of this person's brothers and sisters, excluding
        half-siblings. Siblings are assumed to be full siblings if only one
        parent is known."""
        return Person.objects.filter(
            ~Q(id=self.pk),
            Q(~Q(parent=None), parent__husband=self.parent.husband),
            Q(~Q(parent=None), parent__wife=self.parent.wife),
        ).order_by('date_of_birth')

    def siblings(self):
        """Returns a list of this person's brothers and sisters, excluding
        half-siblings. Siblings are assumed to be full siblings if only one
        parent is known."""
        return Person.objects.filter(
            ~Q(id=self.pk),
            Q(~Q(parent=None), parent__husband=self.parent.husband, parent__wife=self.parent.wife),
        ).order_by('date_of_birth')

    def photos(self):
        """Returns a list of all photos associated with this person."""
        return Photograph.objects.filter(person=self)

    def clean(self):
        if self.date_of_death and not self.deceased:
            raise ValidationError('Cannot specify date of death for living person.')
        if (self.parent and self.parent.husband == self) or (self.parent and self.parent.wife == self):
            raise ValidationError('Person cannot be their own parent.')

    def get_absolute_url(self):
        return reverse('person', args=[self.id])

    def __str__(self):
        return self.name()

    def __repr__(self):
        return self.name()


class Marriage(BaseModel):
    husband = models.ForeignKey(
        Person,
        models.CASCADE,
        limit_choices_to={'gender': 'M'},
        related_name='husband_of'
    )
    wife = models.ForeignKey(
        Person,
        models.CASCADE,
        limit_choices_to={'gender': 'F'},
        related_name='wife_of'
    )
    date = UncertainDateField(blank=True, null=True, help_text="YYYY-MM-DD")
    location = models.ForeignKey(
        "locations.Address",
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='weddings'
    )
    divorced = models.BooleanField(default=False, help_text="Pisah")
    reference = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['husband__surname', 'date']

    def verb(self):
        return 'married'

    def __str__(self):
        return self.husband.name(use_surname=True, use_nickname=False) + ' & ' + self.wife.name(use_surname=False, use_nickname=False)

    def children(self):
        """Returns a list of this person's children."""
        return Person.objects.filter(parent=self).all()


class Photograph(BaseModel):
    """The photograph record combines an image with an optional caption and date
    and links it to one or more people."""
    image = models.ImageField(upload_to='photos', blank=False, null=False)
    people = models.ManyToManyField(Person, related_name='photos')
    caption = models.TextField(blank=True)
    date = UncertainDateField(blank=True, null=True)
    location = models.ForeignKey(
        "locations.Address",
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='photos'
    )

    def __str__(self):
        return self.image.url

    class Meta:
        ordering = ['-date']


class Document(BaseModel):
    BIRTH = 0
    MARRIAGE = 1
    DEATH = 2
    CENSUS = 3
    MILITARY = 4
    LAND = 5
    PRESS = 6
    EMIGRATION = 7

    DOCUMENT_TYPE = [
        (BIRTH, 'Birth'),
        (MARRIAGE, 'Marriage'),
        (DEATH, 'Death/Burial'),
        (CENSUS, 'Census'),
        (MILITARY, 'Military'),
        (LAND, 'Land'),
        (PRESS, 'Press'),
        (EMIGRATION, 'Emigration/Citizenship')
    ]

    file = models.FileField(upload_to='documents', blank=False, null=False)
    document_type = models.PositiveSmallIntegerField(choices=DOCUMENT_TYPE, blank=False, null=False)
    title = models.CharField(max_length=100)
    people = models.ManyToManyField(Person, related_name='documents')

    def file_extension(self):
        _, extension = os.path.splitext(self.file.name)
        return extension[1:]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
