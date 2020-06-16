from datetime import datetime
from django.shortcuts import render  # -> It can send httpResponse Html inside
from django.http import HttpResponse
from . import models

# Create your views here.
def all_rooms(request):
    all_rooms = models.Room.objects.all()
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
    # now = datetime.now()
    # hungry = True
    # return render(request, "all_rooms.html", context={"now": now, "hungry": hungry})
    # now = datetime.now()
    # return HttpResponse(content=f"<h1>{now}</h1>")
    # print(dir(request))
