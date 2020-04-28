from django.shortcuts import render, get_object_or_404
from django.conf import settings
from constructor_app import utils
from constructor_app.models import Template, Order
from mainapp.models import Hotel


def main(request):
    templates = Template.objects.all()
    hotel_id = request.GET['hotel_id']

    return render(request, 'constructor_app/main.html', {'templates': templates, 'hotel_id': hotel_id})


def about_template(request, id):
    # get template
    template = get_object_or_404(Template, id=id)

    # create order for user
    hotel = get_object_or_404(Hotel, id=request.GET['hotel_id'])
    order = Order.objects.create(user=request.user, hotel=hotel, template=template)

    return render(request, 'constructor_app/detail.html', {'template': template, 'order': order})


def pack_project(request, id):
    order = get_object_or_404(Order, user=request.user, id=id)

    # copying projects to zip archive

    if order.status == Order.FORMING:
        utils.zipdir(order.hotel.name, f'{settings.DOMAIN_NAME}/{order.template.path}',
                     f'{settings.BASE_DIR}/media/ready_projects/')

        order.status = Order.READY
        order.save()

    return render(request, 'constructor_app/result.html',
                  {'order': order, 'path': f'{settings.DOMAIN_NAME}/media/ready_projects/{order.hotel.name}.zip'})
