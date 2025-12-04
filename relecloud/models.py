from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Destination(models.Model):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=50
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name


class Cruise(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises'
    )

    def __str__(self):
        return self.name


class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT
    )


class Review(models.Model):
    """
    Review de un usuario sobre un Destination o un Cruise.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews",
    )

    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews",
    )

    title = models.CharField(
        max_length=200,
        blank=True,
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    comment = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        target = self.destination or self.cruise
        return f"Review de {self.user} sobre {target} ({self.rating}⭐)"
