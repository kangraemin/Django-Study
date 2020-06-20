from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import (
    models,
)  # 해당 admin.py 와 같은 directory에 있는 모든 파일 ( apps.py .... )들을 불러오고 그 중에 models.py를 가져온다.

# Register your models here.


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """

    # see the difference is or not in admin pannel
    fieldsets = UserAdmin.fieldsets + (
        (
            (
                "Custom Profile",
                {
                    "fields": (
                        "avatar",
                        "gender",
                        "bio",
                        "birthdate",
                        "language",
                        "currency",
                        "superhost",
                    )
                },
            ),
        )
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
    )
