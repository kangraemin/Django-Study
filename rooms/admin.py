from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        ("Spaces", {"fields": ("amenities", "facilites", "house_rule")},),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("guests", "beds", "bedrooms", "baths",),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    ordering = ("name", "price", "bedrooms")

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos"
        # "amenities", -> many to many fields -> to show count of it, have to write function to count
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilites",
        "house_rule",
        "city",
        "country",
    )

    # django-projcet -> admin pannel ModelAdmin ~
    # icontains search ( default ) ( ^ / = / @ search operator in django admin pannel )
    search_fields = ("=city", "^host__username")

    filter_horizontal = (
        "amenities",
        "facilites",
        "house_rule",
    )

    # self -> Admin class, object -> current row
    def count_amenities(self, object):
        return object.amenities.count()

    def count_photos(self, obj):
        # related name -> photos
        return obj.photos.count()

    # count_amenities.short_description = "HELLO !"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass

