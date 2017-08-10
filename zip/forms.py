from django import forms
from .models import Zip_types, Zip_locations, Zip_systems

class TypesForm(forms.ModelForm):
    class Meta:
        model = Zip_types
        exclude = ()

class LocationsForm(forms.ModelForm):
    class Meta:
        model = Zip_locations
        exclude = ()

class SystemsForm(forms.ModelForm):
    class Meta:
        model = Zip_systems
        exclude = ()


class ZipPostForm (forms.ModelForm)
    def __init__(self, *args, **kwargs):
        nt = kwargs.pop('ntype')
        department = kwargs.pop('dep')
        act = kwargs.pop('act')
        role = kwargs.pop('role')
        only_our = kwargs.pop('only_our')
        super().__init__(*args, **kwargs)
        self.fields['need_start_date'].widget.format = "%d.%m.%Y %H:%M"
        self.fields['need_finish_date'].widget.format = "%d.%m.%Y %H:%M"
        self.fields['latest_date'].widget.format = "%d.%m.%Y"
        self.fields['address'].widget.format = "%d.%m.%Y"
        self.fields['need_type'].widget = forms.HiddenInput()
        self.fields['need_text'] = forms.CharField(label="Особые отметки", required=False,
                                                   widget=forms.Textarea(attrs={'rows': 5}))

        if role == 'write':
            self.fields['boss'].queryset = Boss.objects.filter(dep=department)
            if only_our == True:
                self.fields['car_head'].queryset = Personal.objects.filter(IsBloked=None, fio__contains=' ',
                                                                           dep=department)
                self.fields['slinger'].queryset = Personal.objects.filter(IsBloked=None, fio__contains=' ',
                                                                          dep=department)
            else:
                self.fields['car_head'].queryset = Personal.objects.filter(IsBloked=None, fio__contains=' ')
                self.fields['slinger'].queryset = Personal.objects.filter(IsBloked=None, fio__contains=' ')
            '''if department == 0:
                pass
            else:
                self.fields['dep'].queryset = Department.objects.filter(id = department.id)'''

        if role == 'read':
            self.fields['dep'].widget.attrs['disabled'] = True
            self.fields['purpose'].widget.attrs['disabled'] = True
            self.fields['need_text'].widget.attrs['disabled'] = True
            self.fields['need_start_date'].widget.attrs['disabled'] = True
            self.fields['need_finish_date'].widget.attrs['disabled'] = True
            self.fields['latest_date'].widget.attrs['disabled'] = True
            self.fields['car'].widget.attrs['disabled'] = True
            self.fields['need_vol'].widget.attrs['disabled'] = True
            self.fields['address'].widget.attrs['disabled'] = True
            self.fields['route'].widget.attrs['disabled'] = True
            self.fields['weight'].widget.attrs['disabled'] = True
            self.fields['X'].widget.attrs['disabled'] = True
            self.fields['Y'].widget.attrs['disabled'] = True
            self.fields['Z'].widget.attrs['disabled'] = True
            self.fields['car_head'].widget.attrs['disabled'] = True
            self.fields['slinger'].widget.attrs['disabled'] = True
            self.fields['only_our'].widget.attrs['disabled'] = True
            self.fields['convoy'].widget.attrs['disabled'] = True
            self.fields['load_name'].widget.attrs['disabled'] = True
            self.fields['load_method'].widget.attrs['disabled'] = True
            self.fields['boss'].widget.attrs['disabled'] = True
            self.fields['LEP'].widget.attrs['disabled'] = True
            self.fields['project'].widget.attrs['disabled'] = True
            self.fields['technology'].widget.attrs['disabled'] = True
            self.fields['cfo'].widget.attrs['disabled'] = True
            self.fields['mvz'].widget.attrs['disabled'] = True

        if act == 'add':
            if department == 0:
                pass
            else:
                try:
                    self.fields['car'].initial = Need.objects.filter(dep=department).latest('car').car
                except Need.DoesNotExist:
                    self.fields['car'].initial = 1
                try:
                    self.fields['car_head'].initial = Need.objects.filter(dep=department).latest('car_head').car_head
                except Need.DoesNotExist:
                    pass
                try:
                    self.fields['slinger'].initial = Need.objects.filter(dep=department).latest('slinger').slinger
                except Need.DoesNotExist:
                    pass
                self.fields['dep'].initial = department
                self.fields['cfo'].initial = Department.objects.get(id=department.id).cfo
                try:
                    self.fields['boss'].initial = Need.objects.filter(dep=department).latest('boss').boss
                except Need.DoesNotExist:
                    self.fields['boss'].initial = Boss.objects.filter(dep=department).first()


    class Meta:
        model = Zip_nakl
        fields = ('Zip_types','Zip_locations','Zip_systems')


