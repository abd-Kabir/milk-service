from django.db import models


class CompanyType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'CompanyType'


class Region(models.Model):
    name_uz = models.CharField(max_length=30, blank=True, null=True)
    name_ru = models.CharField(max_length=30, blank=True, null=True)
    name_en = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name_uz

    class Meta:
        db_table = 'Region'


class District(models.Model):
    name_uz = models.CharField(max_length=100, blank=True, null=True)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name_uz

    class Meta:
        db_table = 'District'
