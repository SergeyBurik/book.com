from django.shortcuts import render
from robokassa.forms import RobokassaForm
from mainapp.models import Bookings


def pay_with_robokassa(request, hotel_id, room_id):
    email = request.user.email
    print(email)
    total = sum([booking.room.price for booking in Bookings.objects.filter(room=room_id, hotel=hotel_id)])
    booking_number = Bookings.objects.filter(room=room_id, hotel=hotel_id)[0]
    print('THIS ISSSSSSSSSSSSSSSSSSSSSSSSSs')
    print(total)

    # booking = get_object_or_404(Bookings, hotel__pk=hotel_id, room__pk=room_id, date=check_in)
    #
    # start = datetime.datetime.strptime(check_in, "%Y-%m-%d")
    # end = datetime.datetime.strptime(check_out, "%Y-%m-%d")
    # date_list = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]
    # total = sum([booking.room.price for x in range(len(date_list))])

    form = RobokassaForm(initial={
        'OutSum': total,
        'InvId': booking_number,
        'Desc': 'Some item',
        'Email': request.user or 'user@example.com',
        # 'Email': request.user.email or 'user@example.com',
        # 'UserId': request.user.pk,
        # 'SiteId': 1
    })

    content = {
        'total': total,
        'booking_number': booking_number,
        'form': form,
    }

    return render(request, 'robokassa/form.html', content)


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
