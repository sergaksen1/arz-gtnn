'''
Created on 3 июня 2016 г.

@author: GolnoschekovMA
'''
from dal import autocomplete
from django import forms
from .models import Need, Address, Route, Car, Purpose
from gtnn_base.models import Personal, Boss, Department

class CarForm(forms.ModelForm): 
    class Meta:
        model = Car
        exclude = ('car_kod',)

class PersonalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dep'].widget.attrs['id']='id_dep_pers'
        
    class Meta:
        model = Personal
        exclude = ('fmol', 'IsBloked', 'GUIDSTR', 'aduser_id', 'EmployeeID', 'IsDeleted', 'input_method')

class AddressForm(forms.ModelForm): 
    class Meta:
        model = Address
        exclude = ()
        
class RouteForm(forms.ModelForm): 
    class Meta:
        model = Route
        exclude = ()
        
class PurpForm(forms.ModelForm): 
    class Meta:
        model = Purpose
        exclude = ()


class NeedPostForm(forms.ModelForm): 
    
    def __init__(self, *args, **kwargs):
        nt = kwargs.pop('ntype')
        department = kwargs.pop('dep')
        act = kwargs.pop('act')
        role = kwargs.pop('role')
        only_our = kwargs.pop('only_our')
        super().__init__(*args, **kwargs)
        self.fields['need_start_date'].widget.format="%d.%m.%Y %H:%M"
        self.fields['need_finish_date'].widget.format="%d.%m.%Y %H:%M"
        self.fields['latest_date'].widget.format="%d.%m.%Y"
        self.fields['address'].widget.format="%d.%m.%Y"
        self.fields['need_type'].widget = forms.HiddenInput()
        self.fields['need_text']=forms.CharField(label="Особые отметки", required=False, widget=forms.Textarea(attrs={'rows': 5}))
        
        if role == 'write':
            self.fields['boss'].queryset = Boss.objects.filter(dep = department)
            if only_our == True:
                self.fields['car_head'].queryset = Personal.objects.filter(IsBloked = None, fio__contains=' ', dep = department)
                self.fields['slinger'].queryset = Personal.objects.filter(IsBloked = None, fio__contains=' ', dep = department)
            else:
                self.fields['car_head'].queryset = Personal.objects.filter(IsBloked = None, fio__contains=' ')
                self.fields['slinger'].queryset = Personal.objects.filter(IsBloked = None, fio__contains=' ')
            '''if department == 0:
                pass
            else:
                self.fields['dep'].queryset = Department.objects.filter(id = department.id)'''
        
        if role == 'read':
            self.fields['dep'].widget.attrs['disabled']=True
            self.fields['purpose'].widget.attrs['disabled']=True
            self.fields['need_text'].widget.attrs['disabled']=True
            self.fields['need_start_date'].widget.attrs['disabled']=True
            self.fields['need_finish_date'].widget.attrs['disabled']=True
            self.fields['latest_date'].widget.attrs['disabled']=True
            self.fields['car'].widget.attrs['disabled']=True
            self.fields['need_vol'].widget.attrs['disabled']=True
            self.fields['address'].widget.attrs['disabled']=True
            self.fields['route'].widget.attrs['disabled']=True
            self.fields['weight'].widget.attrs['disabled']=True
            self.fields['X'].widget.attrs['disabled']=True
            self.fields['Y'].widget.attrs['disabled']=True
            self.fields['Z'].widget.attrs['disabled']=True
            self.fields['car_head'].widget.attrs['disabled']=True
            self.fields['slinger'].widget.attrs['disabled']=True
            self.fields['only_our'].widget.attrs['disabled']=True
            self.fields['convoy'].widget.attrs['disabled']=True
            self.fields['load_name'].widget.attrs['disabled']=True
            self.fields['load_method'].widget.attrs['disabled']=True
            self.fields['boss'].widget.attrs['disabled']=True
            self.fields['LEP'].widget.attrs['disabled']=True
            self.fields['project'].widget.attrs['disabled']=True
            self.fields['technology'].widget.attrs['disabled']=True
            self.fields['cfo'].widget.attrs['disabled']=True
            self.fields['mvz'].widget.attrs['disabled']=True

        
        if act == 'add':
            if department == 0:
                pass
            else:
                try:
                    self.fields['car'].initial = Need.objects.filter(dep = department).latest('car').car
                except Need.DoesNotExist:
                    self.fields['car'].initial = 1
                try:
                    self.fields['car_head'].initial = Need.objects.filter(dep = department).latest('car_head').car_head
                except Need.DoesNotExist:
                    pass
                try:
                    self.fields['slinger'].initial = Need.objects.filter(dep = department).latest('slinger').slinger
                except Need.DoesNotExist:
                    pass
                self.fields['dep'].initial = department
                self.fields['cfo'].initial = Department.objects.get(id = department.id).cfo
                try:
                    self.fields['boss'].initial = Need.objects.filter(dep = department).latest('boss').boss
                except Need.DoesNotExist:
                    self.fields['boss'].initial = Boss.objects.filter(dep = department).first()
            
        
        '''Перевозка грузов'''
        if nt == '1':
            self.fields['need_type'].initial = "1"
            del self.fields['need_finish_date']
            del self.fields['need_vol']
            del self.fields['car_head']
            del self.fields['slinger']
            del self.fields['LEP']
            del self.fields['project']
            del self.fields['technology']
            
        '''Перевозка пассажиров'''
        if nt == '2':
            self.fields['need_type'].initial = "2"
            del self.fields['weight']
            del self.fields['X']
            del self.fields['Y']
            del self.fields['Z']
            del self.fields['load_name']
            del self.fields['load_method']
            del self.fields['slinger']
            del self.fields['LEP']
            del self.fields['project']
            del self.fields['technology']
            
        '''Работа грузоподъемной техники/автовышки'''
        if nt == '3' or nt == '4':
            self.fields['purpose'].label = "Характер работ"
            self.fields['car_head'].label = "Ответственное лицо за безопасное производство работ"
            del self.fields['need_finish_date']
            del self.fields['need_vol']
            del self.fields['X']
            del self.fields['Y']
            del self.fields['Z']
            del self.fields['convoy']
            del self.fields['load_name']
            del self.fields['load_method']
            
        if nt == '3':
            self.fields['need_type'].initial = "3"
            self.fields['slinger'].label = "Стропальщик"
            
        if nt == '4':
            self.fields['need_type'].initial = "4"
            self.fields['slinger'].label = "Рабочий люльки"
            
   
        
    class Meta:
        model = Need
        fields = ('need_type','dep','purpose','need_text','need_start_date','need_finish_date','latest_date','car','need_vol','address','route','weight', 'X','Y','Z','car_head', 'slinger', 'only_our', 'convoy','load_name','load_method', 'boss', 'LEP', 'project', 'technology','cfo','mvz')

