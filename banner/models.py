from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


# Banner model to have all information related banner like location, name, specs etc.
class Banner(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Booking period of all banners in 1 table
class BookingPeriod(models.Model):
    banner = models.ForeignKey(Banner)
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()

    def save(self, *args, **kwargs):
        if self.booking_end_date > self.booking_start_date:
            super(BookingPeriod, self).save(*args, **kwargs)
        else:
            raise ValidationError('Booking End date needs to be ahead of Start date')


# All price dates with their respective info
class PricePeriod(models.Model):
    banner = models.ForeignKey(Banner)
    price = models.CharField(max_length=15)
    price_start_date = models.DateField()
    price_end_date = models.DateField()

    def get_booking_period(self):
        return BookingPeriod.objects.filter(banner=self.banner)

    def save(self, *args, **kwargs):
        if self.price_end_date > self.price_start_date:
            booking_periods = self.get_booking_period()
            for booking_period in booking_periods:
                if (booking_period.booking_start_date <= self.price_start_date <=
                    booking_period.booking_end_date) or \
                        (booking_period.booking_start_date <=
                        self.price_start_date <= booking_period.booking_end_date):
                    raise ValidationError('Price intersecting with BookingPeriod')

            super(PricePeriod, self).save(*args, **kwargs)
        else:
            raise ValidationError('Price End date needs to be ahead of Start date')
