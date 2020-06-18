from math import ceil
from datetime import datetime
from django.shortcuts import render, redirect  # -> It can send httpResponse Html inside
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage
from . import models

# Create your views here.
def all_rooms(request):
    # or 1 -> Default value when values is None
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()  # query set is lazy !!!!
    paginator = Paginator(
        room_list, 10, orphans=5
    )  # I want to hide orphans 5 or less -> put them on previous page
    try:
        rooms = paginator.page(
            int(page)
        )  # page() -> raise error when parameter is not number
        # print(vars(rooms.paginator))
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:  # all exception -> use Exception class
        return redirect("/")  # render(request, "rooms/home.html", {"page": rooms})

    # page = int(page or 1)
    # page_size = 10
    # limit = page_size * page
    # offset = limit - page_size
    # # first -> offset / second -> limit -> 모든것 가져 온다음에 20 ~ 30개를 자르는게 아니라, 장고는 lazy load 한다.
    # all_rooms = models.Room.objects.all()[offset:limit]
    # page_count = models.Room.objects.count() / page_size
    # return render(
    #     request,
    #     "rooms/home.html",
    #     context={
    #         "rooms": all_rooms,
    #         "page": page,
    #         "page_count": ceil(page_count),
    #         "page_range": range(1, ceil(page_count)),
    #     },
    # )

    # now = datetime.now()
    # hungry = True
    # return render(request, "all_rooms.html", context={"now": now, "hungry": hungry})
    # now = datetime.now()
    # return HttpResponse(content=f"<h1>{now}</h1>")
    # print(dir(request))
