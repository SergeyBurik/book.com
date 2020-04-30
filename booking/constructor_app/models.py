from django.db import models

from authapp.models import User
from mainapp.models import Hotel


class Template(models.Model):
    name = models.CharField(max_length=100, verbose_name="Template's name")
    price = models.PositiveIntegerField()
    orders = models.PositiveIntegerField(default=0)
    banner = models.ImageField(verbose_name="Template's Image")
    path = models.CharField(max_length=200, verbose_name="Path to template", default="media/projects/...")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    url = models.CharField(verbose_name="URL", max_length=300, null=True)
    token = models.CharField(verbose_name="API Token", max_length=100, null=True, unique=True)
    # path -> in the future
    date_of_expiry = models.DateField(null=True)

    def __str__(self):
        return f'{self.user.name} - {self.hotel.name}'


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(verbose_name='статус',
                              max_length=3,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + ' ' + self.hotel.name
