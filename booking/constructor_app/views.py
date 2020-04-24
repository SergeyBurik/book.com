from django.shortcuts import render, get_object_or_404

# Create your views here.
from constructor_app.models import Template


def main(request):
    templates = Template.objects.all()

    return render(request, 'constructor_app/main.html', {'templates': templates})

def about_template(request, id):
    template = get_object_or_404(Template, id=id)

    return render(request, 'constructor_app/detail.html', {'template': template})
