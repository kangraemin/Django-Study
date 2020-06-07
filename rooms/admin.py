from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    pass


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


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass

