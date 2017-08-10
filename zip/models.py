from django.db import models


# Таблица ввода ЗИП
class Zip_nakl (models.Model):
    zip_types = models.CharField(max_length=32, null=False, blank=False)
    zip_locations = models.CharField(max_length=32, null=False, blank=False)
    zip_systems = models.CharField(max_length=32, null=False, blank=False)

# Справочник типов обектов
class Zip_types (models.Model):
    zipType_name = models.CharField(max_length=32, null=False, blank=False)
    zipType_desc = models.CharField(max_length=32, null=False, blank=False)


# Справочник параметров объекта
class Zip_params (models.Model):
    Par_name = models.CharField(max_length=32, null=False, blank=False)
    Par_desc = models.CharField(max_length=32, null=False, blank=False)
    Par_type = models.IntegerField()

# Справочник мест
class Zip_locations (models.Model):
    Loc_name = models.CharField(max_length=32, null=False, blank=False)

# Справочник систем
class Zip_systems (models.Model):
    Sys_name = models.CharField(max_length=32, null=False, blank=False)

# Справочник пользователей приложения
class ZIP_Users (models.Model):
    Zip_user_name = models.CharField(max_length=32, null=False, blank=False)