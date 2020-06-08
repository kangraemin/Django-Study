from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review model Definition """

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanLiness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        # return self.review
        # return self.room.host.username
        return f"{self.review} - {self.room}"  # self.room -> get's name ( because __str__ )

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanLiness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg."

