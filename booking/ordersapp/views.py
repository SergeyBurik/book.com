from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from mainapp.models import Bookings
import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# def pay_with_robokassa(request, hotel_id, room_id):
#     email = request.user.email
#     print(email)
#     total = sum([booking.room.price for booking in Bookings.objects.filter(room=room_id, hotel=hotel_id)])
#     booking_number = Bookings.objects.filter(room=room_id, hotel=hotel_id)[0]
#     print('THIS ISSSSSSSSSSSSSSSSSSSSSSSSSs')
#     print(total)
#
#     # booking = get_object_or_404(Bookings, hotel__pk=hotel_id, room__pk=room_id, date=check_in)
#     #
#     # start = datetime.datetime.strptime(check_in, "%Y-%m-%d")
#     # end = datetime.datetime.strptime(check_out, "%Y-%m-%d")
#     # date_list = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]
#     # total = sum([booking.room.price for x in range(len(date_list))])
#
#     form = RobokassaForm(initial={
#         'OutSum': total,
#         'InvId': booking_number,
#         'Desc': 'Some item',
#         'Email': request.user or 'user@example.com',
#         # 'Email': request.user.email or 'user@example.com',
#         # 'UserId': request.user.pk,
#         # 'SiteId': 1
#     })
#
#     content = {
#         'total': total,
#         'booking_number': booking_number,
#         'form': form,
#     }
#
#     return render(request, 'robokassa/form.html', content)


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

                stripe.Payout.create(amount=int(total * 0.95),
                                     currency="rub",
                                     # destination=' '.join([card[i:i + 4] for i in range(0, len(card), 4)]),
                                     destination=card,
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
