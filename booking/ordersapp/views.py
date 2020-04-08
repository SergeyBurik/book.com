from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from mainapp.models import Bookings
import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request, hotel_id, room_id, check_in, check_out):
    booking = get_object_or_404(Bookings, hotel__pk=hotel_id, room__pk=room_id, date=check_in)
    start = datetime.datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.datetime.strptime(check_out, "%Y-%m-%d")
    date_list = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]
    total = sum([booking.room.price for x in range(len(date_list))])
    print(total)
    total = int(total) * 100

    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                stripe.Charge.create(
                    amount=total,
                    currency='rub',
                    description='Booking payment',
                    source=token,
                )

                card = booking.room.hotel.user.credit_card

                destination = stripe.Token.create(
                    card={
                        "number": "4242424242424242",
                        "exp_month": 4,
                        "exp_year": 2021,
                        "cvc": "314",
                    },
                )

                print(destination)
                print(destination['id'])

                stripe.Payout.create(amount=int(total * 0.95),
                                     currency="rub",
                                     # destination=' '.join([card[i:i + 4] for i in range(0, len(card), 4)]),
                                     destination=destination['card']['id'],
                                     source_type="card")

                return HttpResponseRedirect(reverse('main:book_room',
                                                    kwargs={
                                                        'hotel_id': hotel_id,
                                                        'room_id': room_id
                                                    })
                                            )
            except Exception as e:
                print(e)
                messages.error(request, "Your card has been declined.")

    return render(request, 'ordersapp/checkout.html', {'total': total / 100})


def main(request):
    user = request.user
    return render(request, 'ordersapp/base.html', {'user': user})


def success(request):
    user = request.user
    bookings = Bookings.objects.all()
    content = {
        'user': user,
        'bookings': bookings,
    }

    return render(request, 'ordersapp/success.html', content)
