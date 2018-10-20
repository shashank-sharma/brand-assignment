from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import BookingPeriod, PricePeriod, Banner


# Forms for views, clean method is as same as models one
class BookingForm(ModelForm):
    class Meta:
        model = BookingPeriod
        fields = ['booking_start_date', 'booking_end_date']

    def clean(self):
        cd = self.cleaned_data

        booking_start_date = cd.get('booking_start_date')
        booking_end_date = cd.get('booking_end_date')
        if booking_end_date < booking_start_date:
            raise ValidationError('Booking End date needs to be ahead of Start date')

        return cd


class PriceForm(ModelForm):
    class Meta:
        model = PricePeriod
        fields = ['price', 'price_start_date', 'price_end_date']

    def __init__(self, banner_id, *args, **kwargs):
        self.banner_id = banner_id
        super(PriceForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data

        price_start_date = cd.get('price_start_date')
        price_end_date = cd.get('price_end_date')

        if price_end_date > price_start_date:
            booking_periods = BookingPeriod.objects.filter(banner=Banner.objects.get(id=self.banner_id))
            for booking_period in booking_periods:
                if (booking_period.booking_start_date <= price_start_date <=
                    booking_period.booking_end_date) or \
                        (booking_period.booking_start_date <=
                        price_start_date <= booking_period.booking_end_date):
                    raise ValidationError('Price intersecting with BookingPeriod')

            return cd
        else:
            raise ValidationError('Price End date needs to be ahead of Start date')