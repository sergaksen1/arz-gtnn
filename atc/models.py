from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from gtnn_base.models import Department,CFO,Personal,Boss,Filial
from datetime import datetime



#Справочник автомобилей
class Car(models.Model):
    car_name = models.CharField('Наименование транспортного средства', max_length=54, unique=True)
    car_kod = models.CharField('Код МИКС', max_length=16, blank=True, null=True)
    
    def __str__(self):
        return self.car_name
    
    class Meta:
        ordering = ['car_name']

#Справочник МВЗ
class MVZ(models.Model):
    filial = models.ForeignKey(Filial, verbose_name = 'Филиал')
    customer = mvz_name = models.CharField('Заказчик услуг', max_length=256)
    expend = models.CharField('Наименование расходов', max_length=512)
    pressmark = models.CharField('Шифр учета МВЗ', max_length=12, unique=True)
    mvz_name = models.CharField('Наименование МВЗ', max_length=128)
    exp_account = models.CharField('Счета учета расходов', max_length=6, blank=True, null=True)
    VAT_account = models.CharField('Счет НДС', max_length=6, blank=True, null=True)

    def __str__(self):
        return self.mvz_name
    
    class Meta:
        ordering = ['mvz_name']


#Справочник адресов
class Address(models.Model):
    address_name = models.CharField('Адрес', max_length=54, unique=True)

    def __str__(self):
        return self.address_name
    
    class Meta:
        ordering = ['address_name']

#Спрвочник маршрутов
class Route(models.Model):
    route_name = models.CharField('Маршрут', max_length=64, unique=True)
    
    def __str__(self):
        return self.route_name
    
    class Meta:
        ordering = ['route_name']
    
#Список целей
class Purpose(models.Model):
    purp_name = models.CharField('Цель', max_length=64, unique=True)
    
    def __str__(self):
        return self.purp_name
    
    class Meta:
        ordering = ['purp_name']

#Предварительные заявки от служб

start_date = datetime.strptime("{:%d.%m.%Y}".format(timezone.now() + timezone.timedelta(days=1))+' 8:00:00','%d.%m.%Y %H:%M:%S')
finish_date = datetime.strptime("{:%d.%m.%Y}".format(timezone.now() + timezone.timedelta(days=1))+' 17:00:00','%d.%m.%Y %H:%M:%S')
latest_date = datetime.strptime("{:%d.%m.%Y}".format(timezone.now() + timezone.timedelta(days=7))+' 8:00:00','%d.%m.%Y %H:%M:%S')

class Need(models.Model):
    address = models.ForeignKey(Address, default=1, verbose_name='Пункт отправления')
    author = models.ForeignKey(User, null=False)
    boss = models.ForeignKey(Boss, verbose_name='Руководитель')
    car = models.ForeignKey(Car, verbose_name='Наименование ТС', null=True)
    car_head = models.ForeignKey(Personal, verbose_name='Старший в машине', related_name="car_head", null=True)
    cfo = models.ForeignKey(CFO, blank=True, null=True,verbose_name='ЦФО')
    convoy = models.CharField('Сопровождение', blank=True, max_length=64)
    dep  = models.ForeignKey(Department,verbose_name='Подразделение-заказчик', db_index=True)
    latest_date = models.DateField('Не позднее чем', default = latest_date)
    LEP = models.IntegerField('Работа вблизи ЛЭП, расстояние, м.', blank=True, null=True)
    load_method = models.IntegerField('Метод погрузки',choices=((1,("ручной")),(2,("механизированный"))), default = 1)
    load_name = models.CharField('Наименование груза', max_length=64)
    mvz = models.ForeignKey(MVZ, blank=True, null=True,verbose_name='Место возникновения затрат (МВЗ)')
    need_finish_date = models.DateTimeField('Дата возвращения', default = finish_date)
    need_start_date = models.DateTimeField('Дата отправления', default = start_date)
    need_text = models.CharField('Особые отметки', blank=True, max_length=512)
    need_type = models.IntegerField('Тип заявки',choices=((1,("На перевозку грузов")),
                                                          (2,("На перевозку пассажиров")),
                                                          (3,("На работу грузоподъемной техники")),
                                                          (4,("На работу автовышки"))), default = 1)
    need_vol = models.IntegerField('Количество человек', default=1)
    project = models.CharField('Наличие утвержденного проекта производства работ на строительно-монтажные работы', blank=True, max_length=64)
    purpose = models.ForeignKey(Purpose, verbose_name='Цель поездки', default = 1)
    putlist = models.CharField('№ Путевого листа', blank=True, max_length=64)
    route = models.ForeignKey(Route, default=1, verbose_name='Маршрут')
    slinger = models.ForeignKey(Personal, verbose_name='Стропальщик', related_name="slinger", null=True)
    status = models.IntegerField('Статус заявки', default=0)
    technology = models.CharField('Наличие утвержденной технологии на погрузку (разгрузку)', blank=True, max_length=64)
    weight = models.IntegerField('Вес груза, кг.', blank=True, null=True)
    X = models.IntegerField('Габариты груза, длина (мм)', blank=True, null=True)
    Y = models.IntegerField('Габариты груза, ширина (мм)', blank=True, null=True)
    Z = models.IntegerField('Габариты груза, высота (мм)', blank=True, null=True)
    need_create_date = models.DateTimeField(null=False, default=timezone.now)
    only_our = models.BooleanField('Только свои', default=True)
    atc_author = models.ForeignKey(User, verbose_name='Диспетчер', related_name="atc_author", null=True)

    class Meta:
        ordering = ['-need_start_date']
#        index_together = [
#            ["book", "author"],
#        ]


    def __str__(self):
        return self.need_start_date.strftime("%Y-%m-%d %H:%M:%S")
