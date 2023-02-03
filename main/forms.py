from django.forms import ModelForm
from .models import Users, Logbook, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date
# from django.db.models.functions import Extract

class CMNewUsersForm(UserCreationForm):
    cmp_id = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    position = forms.Select(attrs={'class':'form-control'})
    class Meta:
        model = User
        fields = ['cmp_id','first_name','last_name','position','email','password1','password2']
        labels = {'cmp_id' : 'Employee ID'}
    
    # def __init__(self,*args, **kwargs):
    #     super(CMNewUsersForm, self).__init__(self,*args, **kwargs)

    #     self.fields['password1'].widget.attrs['class'] = 'form-control'
    #     self.fields['password2'].widget.attrs['class'] = 'form-control'


class UsersForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class LogbookForm(ModelForm):
    # def __init__(self,*args, **kwargs):
    #     self.request = kwargs.pop("request")
    #     super(LogbookForm, self).__init__(*args,**kwargs)

    date = forms.DateField(initial=date.today(),widget=forms.DateInput(attrs={'class':'form-control'}))
    #cmp_id = forms.CharField(disabled=True)
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
        # fields = ['date','cmp_id']
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