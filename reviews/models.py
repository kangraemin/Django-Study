from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review model Definition """

    review = models.TextField()
    Accuracy = models.IntegerField()
    Communication = models.IntegerField()
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

