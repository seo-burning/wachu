from django.db import models
from core.models import TimeStampedModel, User
from pick.models import ChuPickRating, ChuPickAB


class ChuPickRatingResult(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='chu_pick_rating_result_set', default=None)

    chu_pick_rating = models.ForeignKey(
        ChuPickRating, on_delete=models.CASCADE, default=None)

    rating = models.IntegerField(null=True)

    def __str__(self):
        return "{} - rating : {}".format(self.user, self.chu_pick_rating)


class ChuPickABResult(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='chu_pick_AB_result_set', default=None)

    chu_pick_AB = models.ForeignKey(
        ChuPickAB, on_delete=models.CASCADE, default=None)

    pick_AB = models.CharField(max_length=2, choices=(
        ('A', 'A'), ('B', 'B')), null=True)

    def __str__(self):
        return "{} - rating : {}".format(self.user, self.chu_pick_rating)
