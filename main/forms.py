from django.forms import ModelForm
from .models import Logbook, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date

class CMNewUsersForm(UserCreationForm):
    cmp_id = forms.IntegerField(label='Employee ID',widget=forms.NumberInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    position = forms.Select(attrs={'class': 'dropdown-menu'})
    class Meta:
        model = User
        fields = ['cmp_id','first_name','last_name','position','email','password1','password2']
        labels = {}
    

class UpdateUserForm(ModelForm):
    first_name = forms.CharField(disabled=True,widget=forms.TextInput(attrs={'class': 'form-control',}))
    last_name = forms.CharField(disabled=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    position = forms.Select(attrs={'class': 'form-select'})
    custom_disc_1 = forms.IntegerField(label='Descuento 1',widget=forms.NumberInput(attrs={'class':'form-control'}))
    custom_disc_2 = forms.IntegerField(label='Descuento 2',widget=forms.NumberInput(attrs={'class':'form-control'}))
    custom_disc_3 = forms.IntegerField(label='Descuento 3',widget=forms.NumberInput(attrs={'class':'form-control'}))
    custom_disc_4 = forms.IntegerField(label='Descuento 4',widget=forms.NumberInput(attrs={'class':'form-control'}))
    custom_disc_5 = forms.IntegerField(label='Descuento 5',widget=forms.NumberInput(attrs={'class':'form-control'}))
                
    class Meta:
        model = User
        fields = ['first_name','last_name','position','custom_disc_1','custom_disc_2','custom_disc_3','custom_disc_4','custom_disc_5']

class LogbookForm(ModelForm):
    date = forms.DateField(initial=date.today(),widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    route = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    total_hrs_input = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Hours'}))
    total_min_input = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Minutes'}))
    sun_hrs_input = forms.CharField(empty_value=str(0),required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Hours'}))
    sun_min_input = forms.CharField(empty_value=str(0),required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Minutes'}))
    holiday_hrs_input = forms.CharField(empty_value=str(0),required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Hours'}))
    holiday_min_input = forms.CharField(empty_value=str(0),required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Minutes'}))
    libre_hrs_input = forms.CharField(empty_value=str(0),required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Hours'}))
    libre_min_input = forms.CharField(empty_value=str(0),required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Minutes'}))
    sa_hrs_input = forms.CharField(empty_value=str(0),required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Hours'}))
    sa_min_input = forms.CharField(empty_value=str(0),required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Minutes'}))
    remarks = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Remarks'}))

    class Meta:
        model = Logbook
        exclude = ['total_decimal',
        'total_flight_block',
        'total_sun_block',
        'sun_decimal',
        'total_holiday_block',
        'holiday_decimal',
        'total_libre_block',
        'libre_decimal',
        'total_sa_block',
        'sa_decimal','cmp_id'
        ]
        labels = {
        'total_hrs_input' : 'Block Hours',
        'total_min_input' : 'Block Minutes',
        'sun_hrs_input' : 'Sunday (Hours)',
        'sun_min_input' : 'Sunday (Minutes)',
        'holiday_hrs_input' : 'Holiday (Hours)',
        'holiday_min_input' : 'Holiday (Minutes)',
        'libre_hrs_input' : 'LIBRE (Hours)',
        'libre_min_input' : 'LIBRE (Minutes)',
        'sa_hrs_input' : 'SA (Hours)',
        'sa_min_input' : 'SA (Minutes)'
        }