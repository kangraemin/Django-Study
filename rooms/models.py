from django.db import models

from django_countries.fields import CountryField

from core import models as core_models
from users import models as user_models


# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Object Definition """

    class Meta:
        verbose_name_plural = "Room Types"
        ordering = ["created"]
        # ordering = ["-created"]
        # ordering = ["name"]


class Amenity(AbstractItem):

    """ Amenity object Definition  """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility object Definition  """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule object Definition  """

    class Meta:
        verbose_name_plural = "House Rules"


class Photo(core_models.TimeStampedModel):

    """ Photo object Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(
        upload_to="room_photos"
    )  # which folder will be saved in MEDIA ROOT ( uploads/ )
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )  # on delete -> behavior
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilites = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rule = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # Call the real save() method

    def __str__(self):  # it makes to show Room object -> rooms name
        return self.name

    def total_rating(self):
        all_reviews = self.review_set.all()
        if len(all_reviews) == 0:
            return 0
        all_ratings = 0
        for reviews in all_reviews:
            all_ratings += reviews.rating_average()

        return all_ratings / len(all_reviews)
