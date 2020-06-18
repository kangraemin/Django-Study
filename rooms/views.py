from django.views.generic import ListView, DetailView
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect

# from math import ceil
# from datetime import datetime
# from django.shortcuts import render, redirect  # -> It can send httpResponse Html inside
# from django.http import HttpResponse
# from django.core.paginator import Paginator, EmptyPage
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    # https://ccbv.co.uk
    # google -> search django fbv vs cbv !!
    # Choose fbv / cbv proper situation
    model = models.Room
    paginate_by = 10  # paginate
    ordering = "created"
    paginate_orphans = 5
    context_object_name = "rooms"

    # context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

    # page_kwarg = "potato"


# cbv ( abstraction )
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    # Detailview -> find pk automatically in url !!! must be called with pk

    model = models.Room

    # pk_url_kwarg = "potato"  # -> can change pk name
    # 404 error -> automatically render


# fbv
# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404()  # return x / raise o
#         # return redirect(reverse("core:home"))

#     # print(dir(room))


# browser -> 404 인지함

# # Create your views here.
# def all_rooms(request):
#     # or 1 -> Default value when values is None
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()  # query set is lazy !!!!
#     paginator = Paginator(
#         room_list, 10, orphans=5
#     )  # I want to hide orphans 5 or less -> put them on previous page
#     try:
#         rooms = paginator.page(
#             int(page)
#         )  # page() -> raise error when parameter is not number
#         # print(vars(rooms.paginator))
#         return render(request, "rooms/home.html", {"page": rooms})
#     except EmptyPage:  # all exception -> use Exception class
#         return redirect("/")  # render(request, "rooms/home.html", {"page": rooms})

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
