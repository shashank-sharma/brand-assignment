from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from banner.models import Banner, BookingPeriod, PricePeriod
from .forms import BookingForm, PriceForm, BannerForm


@login_required(login_url='/admin')
def home(request):
    if request.method == 'POST':
        banner_form = BannerForm(request.POST)
        if banner_form.is_valid():
            banner_model = Banner()
            banner_model.name = banner_form.cleaned_data['name']
            banner_model.user = request.user
            banner_model.save()
            return HttpResponseRedirect('/')
        banner_list = Banner.objects.filter(user=request.user)
        return render(request, 'home.html', {'banner_list': banner_list, 'form': banner_form})
    else:
        banner_list = Banner.objects.filter(user=request.user)
        banner_form = BannerForm()
        return render(request, 'home.html', {'banner_list': banner_list, 'form': banner_form})


@login_required(login_url='/admin')
def banner(request, banner_id):
    try:
        banner = Banner.objects.get(id=banner_id)
        booking_period = BookingPeriod.objects.filter(banner=banner)
        price_period = PricePeriod.objects.filter(banner=banner)
        return render(request, 'banner.html', {'banner': banner, 'booking_period_list': booking_period,
                                               'price_period_list': price_period})
    except:
        return render(request, '404.html', {})


@login_required(login_url='/admin')
def booking_edit(request, banner_id, booking_id='add'):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            if booking_id == 'add':
                booking_model = BookingPeriod()
            else:
                booking_model = BookingPeriod.objects.get(id=booking_id)
            booking_model.banner = Banner.objects.get(id=banner_id)
            booking_model.booking_start_date = booking_form.cleaned_data['booking_start_date']
            booking_model.booking_end_date = booking_form.cleaned_data['booking_end_date']
            booking_model.save()
            return HttpResponseRedirect('/' + banner_id)
        return render(request, 'banner_edit.html', {'form': booking_form})
    else:
        try:
            if booking_id == 'add':
                booking_form = BookingForm()
            else:
                booking_period = BookingPeriod.objects.get(id=booking_id)
                booking_form = BookingForm(initial={'booking_start_date': booking_period.booking_start_date,
                                                    'booking_end_date': booking_period.booking_end_date})
            return render(request, 'banner_edit.html', {'form': booking_form})
        except:
            return render(request, '404.html', {})


@login_required(login_url='/admin')
def price_edit(request, banner_id, price_id='add'):
    if request.method == 'POST':
        price_form = PriceForm(banner_id=banner_id, data=request.POST)
        if price_form.is_valid():
            if price_id == 'add':
                price_model = PricePeriod()
            else:
                price_model = PricePeriod.objects.get(id=price_id)
            price_model.banner = Banner.objects.get(id=banner_id)
            price_model.price = price_form.cleaned_data['price']
            price_model.price_start_date = price_form.cleaned_data['price_start_date']
            price_model.price_end_date = price_form.cleaned_data['price_end_date']
            price_model.save()
            return HttpResponseRedirect('/' + banner_id)
        return render(request, 'price_edit.html', {'form': price_form})
    else:
        try:
            if price_id == 'add':
                price_form = PriceForm(banner_id=banner_id)
            else:
                price_period = PricePeriod.objects.get(id=price_id)
                price_form = PriceForm(initial={'price_start_date': price_period.price_start_date,
                                                  'price_end_date': price_period.price_end_date})
            return render(request, 'price_edit.html', {'form': price_form})
        except:
            return render(request, '404.html', {})