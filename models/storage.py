from django.db import models


class Storage(models.Model):
    city = models.CharField(max_length=255, verbose_name="Город")
    group = models.CharField(max_length=255, verbose_name="Группа")
    slug = models.SlugField(verbose_name="Ссылка", unique=True)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
