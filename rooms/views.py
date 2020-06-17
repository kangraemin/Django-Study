from datetime import datetime
from django.shortcuts import render  # -> It can send httpResponse Html inside
from django.http import HttpResponse
from . import models

# Create your views here.
def all_rooms(request):
    page = int(request.GET.get("page", 1))
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    # first -> offset / second -> limit -> 모든것 가져 온다음에 20 ~ 30개를 자르는게 아니라, 장고는 lazy load 한다.
    all_rooms = models.Room.objects.all()[offset:limit]
    return render(request, "rooms/home.html", context={"rooms": all_rooms})

    # now = datetime.now()
    # hungry = True
    # return render(request, "all_rooms.html", context={"now": now, "hungry": hungry})
    # now = datetime.now()
    # return HttpResponse(content=f"<h1>{now}</h1>")
    # print(dir(request))
