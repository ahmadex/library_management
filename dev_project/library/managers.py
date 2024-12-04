from django.db import models

class BookManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(title__istartswith='t')