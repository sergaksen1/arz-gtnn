import os
import json

from dal import autocomplete
from docxtpl import DocxTemplate
from datetime import timedelta, date, datetime


from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.utils import timezone

from gtnn_atc.forms import NeedPostForm, CarForm, PersonalForm, PurpForm
from gtnn_auth.models import Profile
from gtnn_base.crumb import BREADCRUMB
from gtnn_base.models import Department, Boss, Personal
from gtnn_base.views import mssql_raw
from gtnn_rac.views import download_xls_dict

from gtnn_atc.models import Need, Address, Route

''' Начало месяца''' 
def first_date(d):
    next_m = date(d.year, d.month, 28) + timedelta(days = 4)
    end = next_m - timedelta(days = next_m.day)
    start = date(end.year, end.month, 1)
    return start

''' Конец месяца''' 
def last_date(d):
    next_m = date(d.year, d.month, 28) + timedelta(days = 4)
    end = next_m - timedelta(days = next_m.day)
    return end

''' Оглавление '''
@login_required
def atc_index(request):
    args = {}
    
#    BREADCRUMB.set([{'title':'Рац.работа','url':''},{'title':'ОТЧЕТЫ','url':reverse('rac:main')}])
    return render(request, 'atc_index.html', args)

''' Главная страница со списком заявок на автотранспорт'''
@login_required
def need_index(request): 
    BREADCRUMB.set([{'title':'АРМ АТЦ', 'url':'#'},{'title':'Просмотр','url':''}])
    d = first_date(datetime.now().date())
    args = {}      
    args.update(csrf(request))
    year = datetime.now().year
    try:
        group = request.user.groups.get().name
    except:
        group = 'none'
    
    if 'submit' in request.GET:
        submit_type = request.GET['submit']
    else:    
        submit_type = 'search'
    
    if 'depzak' in request.GET:
        depzak = int(request.GET['depzak'])
    else:
        try:
            if group == 'atc':
                depzak = 0
            else:
                depzak = request.user.profile.personal.dep.id
        except Profile.DoesNotExist:
            depzak = 0
        except AttributeError:
            depzak = 0
            
    if depzak == 0:
        needs = Need.objects.all()
    else:
        needs = Need.objects.filter(dep_id=depzak)
        
    if 'need_type' in request.GET:
        ntype = int(request.GET['need_type'])
    else:
        ntype = 0
    if ntype != 0:
        needs = needs.filter(need_type=ntype)
        
    if 'start_date' in request.GET:
        start_date = datetime.strptime(request.GET['start_date'],'%d.%m.%Y')
    else:    
        start_date = datetime(year, 1, 1, 0, 0, 0) # 1 января 00:00
    if 'end_date' in request.GET:
        end_date = datetime.strptime(request.GET['end_date']+' 23:59:59','%d.%m.%Y %H:%M:%S')
    else:    
        end_date = datetime(year, 12, 31, 23, 59, 59) # 31 декабря 23:59
    needs = needs.filter(need_start_date__range=[start_date, end_date])
    needs = needs.order_by('-id')
    '''needs = needs.order_by('status')'''
    
    dstart = "{:%d.%m.%Y}".format(start_date)
    dend = "{:%d.%m.%Y}".format(end_date)
    expdate = timezone.now() - timedelta(minutes = 10)
    dep_list = Department.objects.all()
    type_list = dict(Need._meta.get_field('need_type').choices)
    
    need_list = [
                 {'id': n.id,
                  'status': n.status, 
                  'putlist': n.putlist if n.putlist else '', 
                  'atc_author': n.atc_author.username if n.atc_author else '', 
                  'need_start_date': n.need_start_date if n.need_start_date else '', 
                  'need_finish_date': n.need_finish_date if n.need_finish_date else '', 
                  'latest_date': n.latest_date if n.latest_date else '', 
                  'address': n.address.address_name if n.address else '', 
                  'route': n.route.route_name if n.route else '', 
                  'need_type': type_list[n.need_type] if n.need_type else '', 
                  'dep': n.dep.dep_name if n.dep else '', 
                  'cfo': n.cfo.cfo_name if n.cfo else '', 
                  'mvz': n.mvz.mvz_name if n.mvz else '', 
                  'purpose': n.purpose.purp_name if n.purpose else '', 
                  'need_text': n.need_text if n.need_text else '', 
                  'car': n.car.car_name if n.car else '', 
                  'need_vol': n.need_vol if n.need_vol else '', 
                  'boss': n.boss.boss_name.fio if n.boss else '', 
                  'car_head': n.car_head.fio if n.car_head else '', 
                  'slinger': n.slinger.fio if n.slinger else '', 
                  'convoy': n.convoy if n.convoy else '', 
                  'weight': n.weight if n.weight else '', 
                  'X': n.X if n.X else '', 
                  'Y': n.Y if n.Y else '', 
                  'Z': n.Z if n.Z else '', 
                  'load_name': n.load_name if n.load_name else '', 
                  'load_method': n.load_method if n.load_method else '', 
                  'LEP': n.LEP, 
                  'project': n.project, 
                  'technology': n.technology, 
                  'need_create_date': n.need_create_date if n.need_create_date else '', 
                  'author': n.author.username if n.author else ''
                  } for n in needs 
                 ]
        
    paginator = Paginator(needs, 50)
    page = request.GET.get('page')
    try:
        needs = paginator.page(page)
    except PageNotAnInteger:
        needs = paginator.page(1)
    except EmptyPage:
        needs = paginator.page(paginator.num_pages)
        
    field_list = ['id', 'status', 'putlist', 'atc_author', 'need_start_date', 'need_finish_date', 'latest_date', 'address', 'route', 'need_type', 'dep', 'cfo', 'mvz', 'purpose', 'need_text', 'car', 'need_vol', 'boss', 'car_head', 'slinger', 'convoy', 'weight', 'X', 'Y', 'Z', 'load_name', 'load_method', 'LEP', 'project', 'technology', 'need_create_date', 'author']
    field_titles = ['№', 'Статус', 'Путевой лист', 'Диспетчер', 'Время выезда', 'Время возвращения', 'Не позднее чем', 'Место выезда', 'Маршрут', 'Тип заявки', 'Подразделение-заказчик', 'ЦФО', 'МВЗ', 'Цель поездки', 'Особые отметки', 'Транспортное средство', 'Кол-во человек', 'Руководитель', 'Старший в машине', 'Стропальщик', 'Сопровождение', 'Вес груза', 'Длина', 'Ширина', 'Высота', 'Наименование груза', 'Метод погрузки', 'Расстояние до ЛЭП', 'Проект работ', 'Технология на погрузку', 'Дата заявки', 'Автор']    
    xlsfields = ','.join(field_list)
    
    if submit_type == 'В Excel':
        return download_xls_dict(request, need_list, field_list, field_titles)
        
    args['needs'] = needs
    args['depzak'] = depzak
    args['dep_list'] = dep_list
    args['need_type'] = ntype
    args['type_list'] = type_list
    args['start_date'] = dstart
    args['end_date'] = dend
    args['expdate'] = expdate
    args['d'] = d
    args['group'] = group  
    return render(request, 'atc_need.html', args)


''' Добавление путевого листа (ПЛ) '''
@login_required
def pl_add(request):
    try:
        group = request.user.groups.get().name
    except:
        group = 'none'
    if group == 'atc':
        if request.is_ajax():
            if request.method == 'GET':
                pl = request.GET['pl']
                pk = request.GET['pk']
                st = request.GET['st']
                need = Need.objects.get(id = pk)   
                if st == '2':
                    need.status = 2
                    need.atc_author = request.user
                    need.putlist = 'Отклонена!'
                else:
                    if pl:
                        need.status = 1
                        need.atc_author = request.user
                    else:
                        need.status = 0
                        need.atc_author = None
                    need.putlist = pl
                need.save()
    return HttpResponse(pl)


''' Добавление заявки'''    
@login_required
def need_add(request, ntype):
    args = {}
    
    if request.method == "POST":
        submit_type = request.POST['submit']
        d = request.POST['dep']
        dep = Department.objects.get(id = d)
        if submit_type == 'change':
            form = NeedPostForm(ntype = ntype, dep = dep, act = 'add', role = 'write', only_our = True)
        else:
            only_our = request.POST
            form = NeedPostForm(request.POST, ntype = ntype, dep = dep, act = 'add', role = 'write', only_our = only_our)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                pk = post.id
                return redirect('atc:need_edit', pk)
    else:
        dep = request.user.profile.personal.dep if request.user.profile else 0
        form = NeedPostForm(ntype = ntype, dep = dep, act = 'add', role = 'write', only_our = True)
    form1 = CarForm()
    form2 = PersonalForm()
    form3 = PurpForm()
    args['form'] = form
    args['form1'] = form1
    args['form2'] = form2
    args['form3'] = form3
    args['role'] = 'write'
    return render(request, 'atc_need_edit.html', args)

''' Редактирование заявки'''    
@login_required
def need_edit(request, pk):
    #получаем данные о заявке из базы данных
    post = get_object_or_404(Need, pk=pk)
    #проверяем не просрочилась ли заявка
    if post.latest_date < date.today():
        post.status = 2
        post.save()
    #получаем информацию о своём подразделении и проверяем, можно ли редактировать
    try: 
        mydep = request.user.profile.personal.dep
        if post.dep_id == mydep.id and post.status == 0 or post.author == request.user and post.status == 0:
            role = 'write'
        else:
            role = 'read'
    except AttributeError:
        mydep = 0
        role = 'read' 
    ntype = str(post.need_type)
    
    if request.method == "POST":
        #Получаем данные из браузера
        submit_type = request.POST['submit']
        d = request.POST['dep']
        dep = Department.objects.get(id = d)
        only_our = request.POST
        #Если пользователь меняет подразделение-заказчика
        if submit_type == 'change':
            form = NeedPostForm(ntype = ntype, dep = dep, act = 'add', role = 'write', only_our = True)
        else:
            #Если пользователь сохраняет данные
            if post.dep_id == mydep.id or post.author == request.user:
                if role == 'write':
                    form = NeedPostForm(request.POST, instance=post, ntype=ntype, dep = dep, act = 'edit', role = role, only_our = only_our)
                    if form.is_valid():
                        post = form.save(commit=False)
                        post.author = request.user
                        post.need_create_date = datetime.now()
                        post.save()
                    return redirect('atc:need_edit', pk)
            else:
                form = NeedPostForm(instance=post, ntype=ntype, dep = dep, act = 'edit', role = role, only_our = only_our)
    else:
        #Загрузка страницы 
        only_our = post.only_our
        dep = post.dep_id
        form = NeedPostForm(instance=post, ntype=ntype, dep = dep, act = 'edit', role = role, only_our = only_our)   
    args = {} 
    args['pk'] = pk
    args['a'] = 1
    args['post'] = post
    args['form'] = form
    args['form1'] = CarForm()
    args['form2'] = PersonalForm()
    args['form3'] = PurpForm()
    args['role'] = role
    return render(request, 'atc_need_edit.html', args)

''' Удаление заявки'''
@login_required
def need_del(request, need_id = None):
    if need_id:
        del_need = Need.objects.get(id=need_id)
        if del_need.dep_id == request.user.profile.personal.dep.id and del_need.status == 0:
            del_need.delete()
        else:
            pass
    return redirect('atc:need')

''' Копирование заявки'''
@login_required
def need_copy(request, need_id = None):
    if need_id:
        copy_need = Need.objects.get(id=need_id)
        new_need = Need(
            address = copy_need.address,
            author = request.user,
            boss = copy_need.boss,
            car = copy_need.car,
            car_head = copy_need.car_head,
            cfo = copy_need.cfo,
            convoy = copy_need.convoy,
            dep  = copy_need.dep,
            LEP = copy_need.LEP,
            load_method = copy_need.load_method,
            load_name = copy_need.load_name,
            mvz = copy_need.mvz,
            need_text = copy_need.need_text,
            need_type = copy_need.need_type,
            need_vol = copy_need.need_vol,
            project = copy_need.project,
            purpose = copy_need.purpose,
            route = copy_need.route,
            slinger = copy_need.slinger,
            technology = copy_need.technology,
            weight = copy_need.weight,
            X = copy_need.X,
            Y = copy_need.Y,
            Z = copy_need.Z,
            )
        new_need.save()
        pk = new_need.id
    return redirect('atc:need_edit', pk)

''' Чекбокс "Только свои" '''
@login_required
def only_our(request):
    if request.is_ajax():
        if request.method == 'GET':
            check = request.GET['check']
            department = request.GET['dep']
            print(department)
        if check == '1':
            pers = Personal.objects.filter(IsBloked = None, fio__contains=' ', dep = department)
        else:
            pers = Personal.objects.filter(IsBloked = None, fio__contains=' ')
    data = [{'id': p.id,'fio': p.fio} for p in pers]
    return HttpResponse(json.dumps(data), content_type='application/json')

''' Добавление адреса '''
@login_required
def address_add(request):
    name = None
    if request.is_ajax():
        if request.method == 'GET':
            name = request.GET['value']
        if name:
            a = Address(address_name = name)
            a.save()
            x = a.id
    return HttpResponse(x)

''' Добавление маршрута '''
@login_required
def route_add(request):
    name = None
    if request.is_ajax():
        if request.method == 'GET':
            name = request.GET['value']
        if name:
            a = Route(route_name = name)
            a.save()
            x = a.id
    return HttpResponse(x)

''' Добавление транспортного средства '''
@login_required
def car_add(request):
    if request.method == "GET":
        form = CarForm(request.GET)
        a = form.save(commit=False)
        a.save()
        x=a.id
    return HttpResponse(x)

''' Добавление цели '''
@login_required
def purp_add(request):
    if request.method == "GET":
        form = PurpForm(request.GET)
        a = form.save(commit=False)
        a.save()
        x=a.id
    return HttpResponse(x)

''' Получение информации о сотруднике '''
@login_required
def personal(request, pk):
    if request.method == "GET":
        p = get_object_or_404(Personal, pk=pk)
        data = {'id': p.id,
            'fio': p.fio,
            'f': p.f,
            'i': p.i,
            'o': p.o,
            'login_name': p.login_name,
            'tab': p.tab,
            'dep': p.dep.id if p.dep else '',
            'profession': p.profession,
            'place': p.place.id if p.place else '',
            'telephone': p.telephone,
            'mail': p.mail,
            'cert_num': p.cert_num,
            'cert_date': "{:%d.%m.%Y}".format(p.cert_date) if p.cert_date else ''} 
    return  HttpResponse(json.dumps(data), content_type='application/json')

''' Редактирование сотрудника '''
@login_required
def personal_edit(request, pk):
    print('pk=',pk)
    if request.method == "GET":
        '''Новая запись'''
        if pk == '0':
            form = PersonalForm(request.GET)
            if form.is_valid(): 
                pers = form.save(commit=False)
                pers.save()
                print('Добавилась новая запись')
                print(pers)
        else:
            pers = get_object_or_404(Personal, pk=pk)
            form = PersonalForm(request.GET, instance=pers)
            if form.is_valid():
                pers = form.save(commit=False)
                pers.save()
                print('Запись обновлена')
                print(pers)
    data = {'id': pers.id,
            'fio': pers.fio,
            'f': pers.f,
            'i': pers.i,
            'o': pers.o,
            'login_name': pers.login_name,
            'tab': pers.tab,
            'dep': pers.dep.id if pers.dep else '',
            'profession': pers.profession,
            'place': pers.place.id if pers.place else '',
            'telephone': pers.telephone,
            'mail': pers.mail,
            'cert_num': pers.cert_num,
            'cert_date': "{:%d.%m.%Y}".format(pers.cert_date) if pers.cert_date else ''}   
    return HttpResponse(json.dumps(data), content_type='application/json')
    #return HttpResponse(data)
    

''' Автозаполнение (пример) '''
@login_required
class PersonalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Personal.objects.all()

        if self.q:
            qs = qs.filter(fio__istartswith=self.q)

        return qs

'''Экспорт в Word'''
@login_required
def word(request, pk = None):
#    locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
    if pk:
        n = Need.objects.get(id=pk)
        d = n.need_finish_date-n.need_start_date+timedelta(days=1)
        dd = str(d)
        mvz = ''
        v = 0
        weightt = 0
        lep = 'нет'
        project = 'не требуется'
        technology = 'не требуется'
        nt = ''
        car_head_cert_num = ''
        car_head_cert_date = ''
        slinger_cert_num = ''
        slinger_cert_date = ''
        
        if n.mvz:
            mvz = n.mvz
        if n.X and n.Y and n.Z:
            v = round(n.X*n.Y*n.Z/1000000000, 2)
        if n.weight:
            weightt = round(n.weight/1000, 2)  
        if n.LEP:
            lep = n.LEP
        if n.project:
            project = n.project
        if n.technology:
            technology = n.technology    
        if n.need_text:
            nt = n.need_text
        try:
            car_head_cert_num = n.car_head.cert_num
            car_head_cert_date = "{:%d.%m.%Y}".format(n.car_head.cert_date)
            slinger_cert_num = n.slinger.cert_num
            slinger_cert_date = "{:%d.%m.%Y}".format(n.slinger.cert_date)
        except:
            car_head_cert_num =''
            car_head_cert_date = ''
            slinger_cert_num = ''
            slinger_cert_date = ''
            
        context = {'load_name' : n.load_name,
                   'weight_t' : weightt,
                   'weight_kg': n.weight,
                   'X' : n.X,
                   'Y' : n.Y,
                   'Z' : n.Z, 
                   'V' : v,
                   'auto_name' : n.car,
                   'purpose' : n.purpose,
                   'car_head' : n.car_head,
                   'car_head_cert' : car_head_cert_num,
                   'car_head_date' : car_head_cert_date,
                   'slinger' : n.slinger,
                   'slinger_cert' : slinger_cert_num,
                   'slinger_date' : slinger_cert_date,
                   'convoy' : n.convoy,
                   'load_method' : n.get_load_method_display(),
                   'boss' : n.boss,
                   'profession' : n.boss.boss_name.profession,
                   'telephone' : n.boss.boss_name.telephone,
                   'cfo' : n.cfo,
                   'start' : "{:%d.%m.%Y}".format(n.need_start_date),
                   'finish' : "{:%d.%m.%Y}".format(n.need_finish_date),
                   'delta' : dd.split()[0],
                   #'delta' : dd.split()[0]+' '+'день' if int(d)==1 else 'дня' if int(d) in (2,3,4) else 'дней',
                   'vol' : n.need_vol,
                   'date' : "{:%d.%m.%Y}".format(n.need_start_date)+' к '+"{:%H:%M}".format(n.need_start_date),
                   'route' : n.route,
                   'address' : n.address,
                   'dep' : n.dep,
                   'mvz' : mvz,
                   'today' : "{:%d.%m.%Y}".format(date.today()),
                   'LEP' : lep,
                   'project' : project,
                   'technology' : technology,
                   'need_text' : nt 
                   } 
    else:
        context = {}
    doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT,"gtnn_atc/docx-templates/atc%s.docx")%(n.need_type))
    doc.render(context)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=atc.docx'
    doc.save(response)
    return response
    
'''Отчет о расходе топлива'''
@login_required
def atc_report_dep(request):
    args = {}      
    args.update(csrf(request))

    if 'submit' in request.POST:
        submit_type = request.POST['submit']
    else:    
        submit_type = 'Найти'
                  
    if 'start_date' in request.POST:
        start_date = request.POST['start_date']
    else:    
        start_date = "{:%d.%m.%Y}".format(first_date(datetime.now().date()))
        
    if 'end_date' in request.POST:
        end_date = request.POST['end_date']
    else:    
        end_date = "{:%d.%m.%Y}".format(last_date(datetime.now().date()))
        
    if 'depzak' in request.POST:
        depzak = request.POST['depzak']
    else:
        depzak = 'all'
        
    field_list = ['DBZak','Num','Dt','DtStart','DtEnd','DistCity','DistNoCity','DistNoRoad','DistTow','TimeEngine','TimeEngineD','ConsumFuel','ConsumFuelD','ConsumFuelProst','ConsumFuelProstD','ConsumFuelMoto','OstStart','OstEnd','OstStartD','OstEndD','Zaprav','ZapravD','Filial_Info','VW_Info','TypeTS','TypeTS1','State_Info','Vodit_Info','DtCreate','Cel_Info','Marsh_Info','Address','RgWrk','TS_Info','FRegSignTS','NumberAutocade','FMarkFuel','FMarkAddFuel','FTypeFuel','FTypeAddFuel','Dispatcher_Info']
    field_titles = ['Подразделение', 'Филиал', 'Номер ПЛ', 'Дата учета ПЛ', 'Дата выезда', 'Дата возврата', 'Пробег(город)', 'Пробег(загород)', 'Пробег(бездорожье)', 'Пробег(буксировка)', 'Простой на осн. топливе, ч.', 'Простой на доп. топливе, ч.', 'Расход всего (осн. топливо), л.', 'Расход всего (доп. топливо), л.', 'Расход при простое (осн. топливо), л.', 'Расход при простое (доп. топливо), л.', 'Расход по М/счетчику, л.', 'Осн. топливо (выезд), л.', 'Осн. топливо (возврат), л.', 'Доп. топливо (выезд), л.', 'Доп. топливо (возврат), л.', 'Осн. топливо (заправлено), л.', 'Доп. топливо (заправлено), л.', 'Филиал-поставщик',' МВЗ-поставщик', 'Тип ТС', 'Номер ПЛ', 'Состояние', 'Водитель', 'Дата создания ПЛ', 'Цель поездки', 'Маршрут', 'Адрес подачи транспорта', 'Режим работы', 'Транспортное средство', 'Государственный номер', '№ автоколонны', 'Марка осн. топлива', 'Марка доп. топлива', 'Вид осн. топлива', 'Вид доп. топлива', 'Диспетчер']    
    fields = ','.join(field_list)
    dep = ['depzak',]
    xlsfields = dep+field_list

    if depzak == 'all':
        pl_list = mssql_raw("SELECT DISTINCT dbo.fnGetDepZak(kod) as depzak, %s FROM [dbo].[fnGetPLdep]('%s','%s') ORDER BY Num"%(fields, start_date, end_date));
    else:
        pl_list = mssql_raw("select * from (select distinct dbo.fnGetDepZak(Kod) as depzak,* from fnGetPLDep('%s','%s')) t WHERE t.depzak = '%s'"%(start_date, end_date, depzak));
   
    dep_list = mssql_raw("select ZakName from fnGetDep('%s','%s') ORDER BY ZakName"%(start_date, end_date));
    
    if submit_type == 'В Excel':
        return download_xls_dict(request, pl_list, xlsfields, field_titles)
    
    args['start_date'] = start_date
    args['end_date'] = end_date
    args['depzak'] = depzak
    args['dep_list'] = dep_list
    args['pl_list'] = pl_list

    return render(request, 'atc_report_dep.html', args)