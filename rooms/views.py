from datetime import datetime
from django.shortcuts import render  # -> It can send httpResponse Html inside
from django.http import HttpResponse

# Create your views here.
def all_rooms(request):
    return render(request, "all_rooms")
    # now = datetime.now()
    # return HttpResponse(content=f"<h1>{now}</h1>")
    # print(dir(request))
