from django.db import models

class Template(models.Model):
    name = models.CharField(max_length=100, verbose_name="Template's name")
    price = models.PositiveIntegerField()
    orders = models.PositiveIntegerField(default=0)
    banner = models.ImageField(verbose_name="Template's Image")
    path = models.CharField(max_length=200, verbose_name="Path to template", default="media/projects/...")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name