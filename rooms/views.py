from django.views.generic import ListView, DetailView, View
from django.http import Http404
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render, redirect
from django_countries import countries

# from math import ceil
# from datetime import datetime
# from django.shortcuts import render, redirect  # -> It can send httpResponse Html inside
# from django.http import HttpResponse
# from django.core.paginator import Paginator, EmptyPage
from . import models, forms


class HomeView(ListView):

    """ HomeView Definition """

    # https://ccbv.co.uk
    # google -> search django fbv vs cbv !!
    # Choose fbv / cbv proper situation
    model = models.Room
    paginate_by = 12  # paginate
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


class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                print(form.cleaned_data)
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["beds__gte"] = bedrooms

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = superhost

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})

        # Form knows where to search / what need for fields
        # If forms.SearchForm(request.GET) -> Can get all GET parmas through forms
        # unbound form -> are empty forms
        # bounded form -> form connected with data
        # form = forms.SearchForm(request.GET)


# # form api !!
# def search(request):

#     country = request.GET.get("country")

#     if country:
#         form = forms.SearchForm(request.GET)
#         if form.is_valid():
#             print(form.cleaned_data)
#             city = form.cleaned_data.get("city")
#             country = form.cleaned_data.get("country")
#             room_type = form.cleaned_data.get("room_type")
#             price = form.cleaned_data.get("price")
#             guests = form.cleaned_data.get("guests")
#             bedrooms = form.cleaned_data.get("bedrooms")
#             baths = form.cleaned_data.get("baths")
#             instant_book = form.cleaned_data.get("instant_book")
#             superhost = form.cleaned_data.get("superhost")
#             amenities = form.cleaned_data.get("amenities")
#             facilities = form.cleaned_data.get("facilities")

#             filter_args = {}

#             if city != "Anywhere":
#                 filter_args["city__startswith"] = city

#             filter_args["country"] = country

#             if room_type is not None:
#                 filter_args["room_type"] = room_type

#             if price is not None:
#                 filter_args["price__lte"] = price

#             if guests is not None:
#                 filter_args["guests__gte"] = guests

#             if bedrooms is not None:
#                 filter_args["beds__gte"] = bedrooms

#             if baths is not None:
#                 filter_args["baths__gte"] = baths

#             if instant_book is True:
#                 filter_args["instant_book"] = True

#             if superhost is True:
#                 filter_args["host__superhost"] = superhost

#             for amenity in amenities:
#                 filter_args["amenities"] = amenity

#             for facility in facilities:
#                 filter_args["facilities"] = facility

#             rooms = models.Room.objects.filter(**filter_args)
#     else:
#         form = forms.SearchForm()

#     # Form knows where to search / what need for fields
#     # If forms.SearchForm(request.GET) -> Can get all GET parmas through forms
#     # unbound form -> are empty forms
#     # bounded form -> form connected with data
#     # form = forms.SearchForm(request.GET)

#     return render(request, "rooms/search.html", {"form": form, "rooms": rooms})


# def search(request):
#     print(request.GET)
#     city = request.GET.get("city", "Anywhere")
#     city = str.capitalize(city)
#     country = request.GET.get("country", "KR")
#     room_type = int(request.GET.get("room_type", 0))
#     room_types = models.RoomType.objects.all()
#     price = int(request.GET.get("price", 0))
#     guests = int(request.GET.get("guests", 0))
#     beds = int(request.GET.get("beds", 0))
#     bedrooms = int(request.GET.get("bedrooms", 0))
#     baths = int(request.GET.get("baths", 0))
#     s_amenities = request.GET.getlist("amenities")
#     s_facilities = request.GET.getlist("facilities")
#     instant = bool(request.GET.getlist("instant", False))
#     superhost = bool(request.GET.getlist("superhost", False))

#     # print(s_amenities, s_facilities)
#     # Feild look up
#     # Forms api !!

#     amenities = models.Amenity.objects.all()
#     facilities = models.Facility.objects.all()

#     form = {
#         "city": city,
#         "s_room_type": room_type,
#         "s_country": country,
#         "s_amenities": s_amenities,
#         "s_facilities": s_facilities,
#         "instant": instant,
#         "superhost": superhost,
#     }

#     choice = {
#         "countries": countries,
#         "room_types": room_types,
#         "amenities": amenities,
#         "facilities": facilities,
#     }

#     filter_args = {}

#     if city != "Anywhere":
#         filter_args["city__startswith"] = city

#     filter_args["country"] = country

#     if room_type != 0:
#         filter_args[
#             "room_type__pk__exact"
#         ] = room_type  # exact -> it must be same exactly( room type is foreign key )

#     if price != 0:
#         filter_args["price__lte"] = price

#     if guests != 0:
#         filter_args["guests__gte"] = guests

#     if bedrooms != 0:
#         filter_args["beds__gte"] = bedrooms

#     if baths != 0:
#         filter_args["baths__gte"] = baths

#     if instant is True:
#         filter_args["instant_book"] = True

#     if superhost is True:
#         filter_args["host__superhost"] = superhost

#     if len(s_amenities) > 0:
#         for s_amenity in s_amenities:
#             filter_args["amenities__pk"] = int(s_amenity)

#     if len(s_facilities) > 0:
#         for s_facility in s_facilities:
#             filter_args["facilities__pk"] = int(s_facility)

#     print(s_amenities)

#     print(filter_args)

#     rooms = models.Room.objects.filter(**filter_args)

#     print(rooms)

#     # print(countries)

#     # qs = models.Room.objects.filter()

#     # if price != 0: #  qs = models.Room.objects.filter().filter(price__lte=price)
#     #     qs = qs.filter(price__lte=price)

#     return render(
#         request,
#         "rooms/search.html",
#         {
#             **form,
#             **choice,
#             "rooms": rooms,
#             "price": price,
#             "guests": guests,
#             "beds": beds,
#             "bedrooms": bedrooms,
#             "baths": baths,
#         },
#     )


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
