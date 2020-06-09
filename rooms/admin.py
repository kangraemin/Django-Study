from django.contrib import admin
from django.utils.html import mark_safe
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


# class PhotoInline(admin.StackedInline):

#     model = models.Photo


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    inlines = (PhotoInline,)

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
        "count_photos",
        "total_rating",
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

    raw_id_fields = ("host",)  # maybe you don't want to loooong fields

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

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # print(dir(obj.file))
        # print(type(obj.file))
        # return f'<img src="{obj.file.url}"/>' -> django protect html hacking
        return mark_safe(f'<img width="50px" src="{obj.file.url}"/>')

    get_thumbnail.short_description = "Thumbnail"

