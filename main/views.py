from multiprocessing import context
import re
from datetime import datetime, timedelta
import calendar
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Logbook, User
from .forms import LogbookForm,CMNewUsersForm, UpdateUserForm
from django.db.models import Sum,Count

# Date on Navbar
def today_date(request):
    today_is2 = datetime.today()
    return render (request,'paybud/templates/navbar.html', {'today_is2' : today_is2})

# Render Home
def home(request):
    home_total = Logbook.objects.aggregate(Sum('total_decimal'))
    home_total_hours_logged = round(home_total['total_decimal__sum'],2)
    home_users = User.objects.aggregate(Count('cmp_id'))
    home_total_users_reg = home_users['cmp_id__count']
    return render(request, 'main/home.html',{'home_total_hours_logged' : home_total_hours_logged,'home_total_users_reg' : home_total_users_reg})

# WIP Calculator
def simplecalc(request):
    sc_block = request.GET.get('t_block')
    sc_sunday = request.GET.get('t_sun')
        
    context = {'sc_block' : sc_block,'sc_sunday' : sc_sunday}
    return render(request,'main/simple_calc.html', context)

# Login & Authenticate User
def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('logbook_calc')
        else:
            messages.error(request, 'Invalid Username OR Password')

    context = {'page' : page}
    return render(request,'main/login_users.html', context)

# Logout User
def logoutUser(request):
    logout(request)
    return redirect('home')

# Register New User
def registeruser(request):
    form = CMNewUsersForm()

    if request.method == 'POST':
        form = CMNewUsersForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = user.first_name.capitalize()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error ocurred during Registration. Try again or contact Administrator')
    return render (request, 'main/login_users.html', {'form':form})

    

@login_required(login_url='login')
def logbook_calc(request):
    curr_month = datetime.now().month
    m = request.GET.get('m') 
    if m == None:
        m = curr_month
    else:
        m = request.GET.get('m')
    sel_month = calendar.month_name[int(m)]
    today_is = datetime.today()
    logform = LogbookForm()
    logbook = Logbook.objects.filter(cmp_id=request.user,date__month=m).order_by('date')
    disc1 = User.objects.filter(cmp_id=request.user)
    disc11 = disc1.aggregate(Sum('custom_disc_1')).get('custom_disc_1__sum',0)
    disc2 = User.objects.filter(cmp_id=request.user)
    disc22 = disc2.aggregate(Sum('custom_disc_2')).get('custom_disc_2__sum',0)
    disc3 = User.objects.filter(cmp_id=request.user)
    disc33 = disc3.aggregate(Sum('custom_disc_3')).get('custom_disc_3__sum',0)
    disc4 = User.objects.filter(cmp_id=request.user)
    disc44 = disc4.aggregate(Sum('custom_disc_4')).get('custom_disc_4__sum',0)
    disc5 = User.objects.filter(cmp_id=request.user)
    disc55 = disc5.aggregate(Sum('custom_disc_5')).get('custom_disc_5__sum',0)
    total_personal_discount = disc11 + disc22 + disc33 + disc44 + disc55
    home_total = Logbook.objects.aggregate(Sum('total_decimal'))
    home_total_hours_logged = round(home_total['total_decimal__sum'],2)
    bill_hrs_block = Logbook.objects.filter(cmp_id=request.user,date__month=m).aggregate(Sum('total_decimal'))
    home_total_hours_logged = Logbook.objects.aggregate(Sum('total_decimal'))
    home_total_users_registered = User.objects.aggregate(Count('cmp_id'))
    try :
        sum_block = round(bill_hrs_block['total_decimal__sum'],2)
    except :
            sum_block = 66.00
    bill_hrs_sunday = Logbook.objects.filter(cmp_id=request.user,date__month=m).aggregate(Sum('sun_decimal'))
    try:
        sum_sunday = round(bill_hrs_sunday['sun_decimal__sum'],2)
    except:
        sum_sunday = 0
    bill_hrs_holiday = Logbook.objects.filter(cmp_id=request.user,date__month=m).aggregate(Sum('holiday_decimal'))
    try:
        sum_holiday = round(bill_hrs_holiday['holiday_decimal__sum'],2)
    except:
        sum_holiday = 0
    bill_hrs_libre = Logbook.objects.filter(cmp_id=request.user,date__month=m).aggregate(Sum('libre_decimal'))
    try:
        sum_libre = round(bill_hrs_libre['libre_decimal__sum'],2)
    except:
        sum_libre = 0
    bill_hrs_sa = Logbook.objects.filter(cmp_id=request.user,date__month=m).aggregate(Sum('sa_decimal'))
    try:
        sum_sa = round(bill_hrs_sa['sa_decimal__sum'],2)
    except:
        sum_sa = 0
    if sum_block <=66:
        block_extra = 0
    else : block_extra = sum_block - 66
    c_base = 3500.00
    c_g_rep = 2663.00 #CC 2023
    c_prima = 650.00
    c_viatico = 1998.00 #CC 2023
    c_viatico_extra = 18.00
    c_prima_extra = 85.31
    c_rata = round((c_base + c_g_rep)/ 75,2)
    c_viatico_variable = round(float(block_extra) * c_viatico_extra,2)
    c_prima_variable = round(float(block_extra) * c_prima_extra,2)
    c_rec_dom = round((float(sum_sunday)*0.5)*c_rata,2)
    c_rec_libre = round((float(sum_libre)*0.5)*c_rata,2)
    c_rec_sa = round((float(sum_sa)*0.5)*c_rata,2)
    c_rec_nac = round((float(sum_holiday)*0.5)*c_rata,2)
    fo_atp_base = 1915.00
    fo_atp_grep = 1342.00 #CC 2023
    fo_atp_prima = 264.00
    fo_atp_viatico = 1370.00 #CC 2023
    fod_natp_grep = 1212.00 #CC 2023
    fo_natp_grep = 48.00 #CC 2023
    fo_atp_viatico_extra = 13.00
    fo_atp_prima_extra= 32.20
    fo_atp_rata = round((fo_atp_base + fo_atp_grep)/75,2)
    fod_natp_rata = round((fo_atp_base + fod_natp_grep)/75,2)
    fo_natp_rata = round(fo_atp_base / 75)
    css_pa = 0.0975
    s_educ = 0.0125
    unpac = 0.01
    fo_isr = round((((((fo_atp_base)/2+fo_atp_viatico+fo_atp_prima+723.42)*13)-11000)*0.15)/13,2)
    c_isr = round((((((c_base)/2+c_viatico+c_prima+1652.96)*13)-50000)*0.25)/13,2)
    isr_grep = 0.1
    fod_natp_rec_dom = round((float(sum_sunday) * 0.5)*fod_natp_rata,2)
    fo_atp_rec_dom = round((float(sum_sunday)*0.5)*fo_atp_rata,2)
    fo_viatico_extra = round(float(block_extra) * fo_atp_viatico_extra,2)
    fo_prima_extra = round(float(block_extra) * fo_atp_prima_extra,2)
    fod_natp_rec_libre = round((float(sum_libre)*0.5)*fod_natp_rata,2)
    fod_natp_rec_sa = round((float(sum_sa)*0.5)*fod_natp_rata,2)
    fod_natp_rec_nac = round((float(sum_holiday)*1.5)*fod_natp_rata,2)
    fo_natp_rec_dom = round((float(sum_sunday)*0.5)*fo_natp_rata,2)
    fo_natp_rec_libre = round((float(sum_libre)*0.5)*fo_natp_rata,2)
    fo_natp_rec_sa = round((float(sum_sa)*0.5)*fo_natp_rata,2)
    fo_natp_rec_nac = round((float(sum_holiday)*1.5)*fo_natp_rata,2)
    fo_atp_rec_libre = round((float(sum_libre)*0.5)*fo_atp_rata,2)
    fo_atp_rec_sa = round((float(sum_sa)*0.5)*fo_atp_rata,2)
    fo_atp_rec_nac = round((float(sum_holiday)*1.5)*fo_atp_rata,2)
    fod_natp_subt = round((fo_atp_base / 2) + (fod_natp_grep / 2) + fo_atp_prima + fo_atp_viatico + fo_viatico_extra + fo_prima_extra + fod_natp_rec_dom + fod_natp_rec_libre + fod_natp_rec_sa + fod_natp_rec_nac,2)
    fo_natp_subt = round((fo_atp_base / 2) + fo_atp_prima + fo_atp_viatico + fo_viatico_extra + fo_prima_extra + fo_natp_rec_dom + fo_natp_rec_libre + fo_natp_rec_sa + fo_natp_rec_nac,2)
    fo_atp_subt = round((fo_atp_base / 2) + (fo_atp_grep / 2) + fo_atp_prima + fo_atp_viatico + fo_viatico_extra + fo_prima_extra + fo_atp_rec_dom + fo_atp_rec_libre + fo_atp_rec_sa + fo_atp_rec_nac,2)
    c_subt = round((c_base / 2) + (c_g_rep / 2) + c_prima + c_viatico + c_viatico_variable + c_prima_variable + c_rec_dom + c_rec_libre + c_rec_sa + c_rec_nac,2)
    c_css = round(((c_base/2)+ (c_g_rep/2) + c_rec_dom + c_rec_libre + c_rec_sa + c_rec_nac)*css_pa,2)
    c_seduc = round(((c_base/2) + c_rec_dom + c_rec_libre + c_rec_sa)*s_educ,2)
    c_unpac = round(c_base * unpac,2)
    c_isr_gr = round(((c_g_rep/2) * isr_grep),2)
    fo_atp_css = round(((fo_atp_base/2)+(fo_atp_grep/2)+fo_atp_rec_dom+fo_atp_rec_libre+fo_atp_rec_sa+fo_atp_rec_nac)*css_pa,2)
    fo_atp_seduc = round(((fo_atp_base/2)+fo_atp_rec_dom+fo_atp_rec_libre+fo_atp_rec_sa+fo_atp_rec_nac)*s_educ,2)
    fo_atp_unpac = round(fo_atp_base * unpac,2)
    fo_atp_isr_gr = round((fo_atp_grep/2)*isr_grep,2)
    fo_natp_css = round(((fo_atp_base/2)+fo_natp_rec_dom+fo_natp_rec_libre+fo_natp_rec_sa+fo_natp_rec_nac)*css_pa,2)
    fo_natp_seduc = round(((fo_atp_base/2)+fo_natp_rec_dom+fo_natp_rec_libre+fo_natp_rec_sa+fo_natp_rec_nac)*s_educ,2)
    fo_natp_unpac = round(fo_atp_base * unpac,2)
    fod_natp_unpac = round(fo_atp_base * unpac,2)
    fod_natp_isr_gr = round((fod_natp_grep/2)*isr_grep,2)
    fo_natp_isr_gr = round((fo_natp_grep/2)*isr_grep,2) #CC 2023
    fod_natp_seduc = round(((fo_atp_base/2)+fod_natp_rec_dom+fod_natp_rec_libre+fod_natp_rec_sa+fod_natp_rec_nac)*s_educ,2)
    fod_natp_css = round(((fo_atp_base/2)+(fod_natp_grep/2)+fod_natp_rec_dom+fod_natp_rec_libre+fod_natp_rec_sa+fod_natp_rec_nac)*css_pa,2)
    c_total_descuentos = round(c_css+c_seduc+c_isr_gr+c_unpac+c_isr+float(total_personal_discount),2)
    fo_atp_total_descuentos = round(fo_atp_css+fo_atp_seduc+fo_atp_isr_gr+fo_atp_unpac+fo_isr+float(total_personal_discount),2)
    fo_natp_total_deducciones = round(fo_natp_css+fo_natp_seduc+fo_natp_isr_gr+fo_natp_unpac+fo_isr+float(total_personal_discount),2)
    fod_natp_total_deducciones = round(fod_natp_css+fod_natp_seduc+fod_natp_isr_gr+fod_natp_unpac+fo_isr+float(total_personal_discount),2)
    c_neto = round(c_subt - c_total_descuentos,2)
    fod_natp_neto = round(fod_natp_subt - fod_natp_total_deducciones,2)
    fo_natp_neto = round(fo_natp_subt - fo_natp_total_deducciones,2)
    fo_atp_neto = round(fo_atp_subt - fo_atp_total_descuentos,2)
    

# Save Form
    if request.method == 'POST':
        logform = LogbookForm(request.POST)
        if logform.is_valid():
            cmp_id = logform.save(commit=False)
            cmp_id.cmp_id = request.user
            cmp_id.save()
            messages.success(request,'Entry recorded Successfully!')
            return redirect('logbook_calc') 
        
    context = {
        'total_personal_discount':total_personal_discount,
        'disc11' : disc11,
        'disc22':disc22,
        'disc33':disc33,
        'disc44':disc44,
        'disc55':disc55,
        'home_total_hours_logged': home_total_hours_logged,
        'home_total_users_registered': home_total_users_registered,
        'c_isr' : c_isr,
        'fo_isr':fo_isr,
        'sel_month' : sel_month,
        'logform': logform,
        'logbook': logbook,
        'sum_block' : sum_block,
        'sum_sunday' : sum_sunday,
        'sum_holiday' : sum_holiday,
        'sum_libre' : sum_libre,
        'sum_sa' : sum_sa,
        'c_base' : c_base,
        'c_g_rep' : c_g_rep,
        'c_prima' : c_prima,
        'c_viatico' : c_viatico,
        'c_viatico_extra' : c_viatico_extra,
        'c_prima_extra' : c_prima_extra,
        'c_rata' : c_rata,
        'c_viatico_variable' : c_viatico_variable,
        'c_prima_variable' : c_prima_variable,
        'c_rec_dom' : c_rec_dom,
        'c_rec_libre' : c_rec_libre,
        'c_rec_sa' : c_rec_sa,
        'c_rec_nac' : c_rec_nac,
        'fo_atp_base' : fo_atp_base,
        'fo_atp_grep' : fo_atp_grep,
        'fo_natp_grep' : fo_natp_grep, #CC 2023
        'fo_atp_prima' : fo_atp_prima,
        'fo_atp_viatico' : fo_atp_viatico,
        'fo_atp_viatico_extra' : fo_atp_viatico_extra,
        'fo_atp_prima_extra' : fo_atp_prima_extra,
        'fod_natp_grep' : fod_natp_grep,
        'fo_atp_rata' : fo_atp_rata,
        'fod_natp_rata' : fod_natp_rata,
        'fo_natp_rata' : fo_natp_rata,
        'fod_natp_rec_dom' : fod_natp_rec_dom,
        'fo_atp_rec_dom' : fo_atp_rec_dom,
        'block_extra' : block_extra,
        'fo_viatico_extra' : fo_viatico_extra,
        'fo_prima_extra' : fo_prima_extra,
        'fod_natp_rec_libre' : fod_natp_rec_libre,
        'fod_natp_rec_sa' : fod_natp_rec_sa,
        'fod_natp_rec_nac' : fod_natp_rec_nac,
        'fo_natp_rec_dom' : fo_natp_rec_dom,
        'fo_natp_rec_libre' : fo_natp_rec_libre,
        'fo_natp_rec_sa' : fo_natp_rec_sa,
        'fo_natp_rec_nac' : fo_natp_rec_nac,
        'fo_atp_rec_libre' : fo_atp_rec_libre,
        'fo_atp_rec_sa' : fo_atp_rec_sa,
        'fo_atp_rec_nac' : fo_atp_rec_nac,
        'fod_natp_subt' : fod_natp_subt,
        'fo_natp_subt' : fo_natp_subt,
        'fo_atp_subt' : fo_atp_subt,
        'c_subt' : c_subt,
        'c_css' : c_css,
        'c_seduc' : c_seduc,
        'c_unpac' : c_unpac,
        'c_isr_gr' : c_isr_gr,
        'fo_atp_css' : fo_atp_css,
        'fo_atp_seduc' :fo_atp_seduc,
        'fo_atp_unpac' : fo_atp_unpac,
        'fo_atp_isr_gr' : fo_atp_isr_gr, 
        'fo_natp_isr_gr' : fo_natp_isr_gr, #CC 2023
        'fo_natp_css' : fo_natp_css,
        'fo_natp_seduc' : fo_natp_seduc,
        'fo_natp_unpac' : fo_natp_unpac,
        'fod_natp_css' : fod_natp_css,
        'fod_natp_seduc' : fod_natp_seduc,
        'fod_natp_isr_gr' : fod_natp_isr_gr,
        'fod_natp_unpac' : fod_natp_unpac,
        'c_total_descuentos' : c_total_descuentos,
        'fo_atp_total_descuentos' : fo_atp_total_descuentos,
        'fo_natp_total_deducciones' : fo_natp_total_deducciones,
        'fod_natp_total_deducciones' : fod_natp_total_deducciones,
        'c_neto' : c_neto,
        'fod_natp_neto' : fod_natp_neto,
        'fo_natp_neto': fo_natp_neto,
        'fo_atp_neto' : fo_atp_neto,
        'today_is' : today_is
    }
    return render(request,'main/logbook_calc.html', context)

# WIP Reserva
@login_required(login_url='login')
def logbook_calc_reserve(request):
    curr_month = datetime.now().month
    m = request.GET.get('m') 
    if m == None:
        m = curr_month
    else:
        m = request.GET.get('m')
    sel_month = calendar.month_name[int(m)]
    today_is = datetime.today()
    logform = LogbookForm()
    logbook = Logbook.objects.filter(cmp_id=request.user,date__month=m).order_by('date')
    bill_hrs_block = Logbook.objects.filter(cmp_id=request.user,date__month=m).aggregate(Sum('total_decimal'))
    try :
        sum_block = round(bill_hrs_block['total_decimal__sum'],2)+4
    except :
            sum_block = 66.00
    bill_hrs_sunday = Logbook.objects.filter(cmp_id=request.user,date__month=m).aggregate(Sum('sun_decimal'))
    try:
        sum_sunday = round(bill_hrs_sunday['sun_decimal__sum'],2)
    except:
        sum_sunday = 0
    bill_hrs_holiday = Logbook.objects.filter(cmp_id=request.user,date__month=m).aggregate(Sum('holiday_decimal'))
    try:
        sum_holiday = round(bill_hrs_holiday['holiday_decimal__sum'],2)
    except:
        sum_holiday = 0
    bill_hrs_libre = Logbook.objects.filter(cmp_id=request.user,date__month=m).aggregate(Sum('libre_decimal'))
    try:
        sum_libre = round(bill_hrs_libre['libre_decimal__sum'],2)
    except:
        sum_libre = 0
    bill_hrs_sa = Logbook.objects.filter(cmp_id=request.user,date__month=m).aggregate(Sum('sa_decimal'))
    try:
        sum_sa = round(bill_hrs_sa['sa_decimal__sum'],2)
    except:
        sum_sa = 0
    if sum_block <=66:
        block_extra = 0
    else : block_extra = sum_block - 66
    c_base = 3500.00
    c_g_rep = 2613.00
    c_prima = 650.00
    c_viatico = 1848.00
    c_viatico_extra = 18.00
    c_prima_extra = 85.31
    c_rata = round((c_base + c_g_rep)/ 75,2)
    c_viatico_variable = round(float(block_extra) * c_viatico_extra,2)
    c_prima_variable = round(float(block_extra) * c_prima_extra,2)
    c_rec_dom = round((float(sum_sunday)*0.5)*c_rata,2)
    c_rec_libre = round((float(sum_libre)*0.5)*c_rata,2)
    c_rec_sa = round((float(sum_sa)*0.5)*c_rata,2)
    c_rec_nac = round((float(sum_holiday)*0.5)*c_rata,2)
    fo_atp_base = 1915.00
    fo_atp_grep = 1293.53
    fo_atp_prima = 264.00
    fo_atp_viatico = 1338.00
    fod_natp_grep = 1163.53
    fo_atp_viatico_extra = 13.00
    fo_atp_prima_extra= 32.20
    fo_atp_rata = round((fo_atp_base + fo_atp_grep)/75,2)
    fod_natp_rata = round((fo_atp_base + fod_natp_grep)/75,2)
    fo_natp_rata = round(fo_atp_base / 75)
    css_pa = 0.0975
    s_educ = 0.0125
    unpac = 0.01
    fo_isr = round((((((fo_atp_base)/2+fo_atp_viatico+fo_atp_prima+723.42)*13)-11000)*0.15)/13,2)
    c_isr = round((((((c_base)/2+c_viatico+c_prima+1652.96)*13)-50000)*0.25)/13,2)
    isr_grep = 0.1
    fod_natp_rec_dom = round((float(sum_sunday) * 0.5)*fod_natp_rata,2)
    fo_atp_rec_dom = round((float(sum_sunday)*0.5)*fo_atp_rata,2)
    fo_viatico_extra = round(float(block_extra) * fo_atp_viatico_extra,2)
    fo_prima_extra = round(float(block_extra) * fo_atp_prima_extra,2)
    fod_natp_rec_libre = round((float(sum_libre)*0.5)*fod_natp_rata,2)
    fod_natp_rec_sa = round((float(sum_sa)*0.5)*fod_natp_rata,2)
    fod_natp_rec_nac = round((float(sum_holiday)*1.5)*fod_natp_rata,2)
    fo_natp_rec_dom = round((float(sum_sunday)*0.5)*fo_natp_rata,2)
    fo_natp_rec_libre = round((float(sum_libre)*0.5)*fo_natp_rata,2)
    fo_natp_rec_sa = round((float(sum_sa)*0.5)*fo_natp_rata,2)
    fo_natp_rec_nac = round((float(sum_holiday)*1.5)*fo_natp_rata,2)
    fo_atp_rec_libre = round((float(sum_libre)*0.5)*fo_atp_rata,2)
    fo_atp_rec_sa = round((float(sum_sa)*0.5)*fo_atp_rata,2)
    fo_atp_rec_nac = round((float(sum_holiday)*1.5)*fo_atp_rata,2)
    fod_natp_subt = round((fo_atp_base / 2) + (fod_natp_grep / 2) + fo_atp_prima + fo_atp_viatico + fo_viatico_extra + fo_prima_extra + fod_natp_rec_dom + fod_natp_rec_libre + fod_natp_rec_sa + fod_natp_rec_nac,2)
    fo_natp_subt = round((fo_atp_base / 2) + fo_atp_prima + fo_atp_viatico + fo_viatico_extra + fo_prima_extra + fo_natp_rec_dom + fo_natp_rec_libre + fo_natp_rec_sa + fo_natp_rec_nac,2)
    fo_atp_subt = round((fo_atp_base / 2) + (fo_atp_grep / 2) + fo_atp_prima + fo_atp_viatico + fo_viatico_extra + fo_prima_extra + fo_atp_rec_dom + fo_atp_rec_libre + fo_atp_rec_sa + fo_atp_rec_nac,2)
    c_subt = round((c_base / 2) + (c_g_rep / 2) + c_prima + c_viatico + c_viatico_variable + c_prima_variable + c_rec_dom + c_rec_libre + c_rec_sa + c_rec_nac,2)
    c_css = round(((c_base/2)+ (c_g_rep/2) + c_rec_dom + c_rec_libre + c_rec_sa + c_rec_nac)*css_pa,2)
    c_seduc = round(((c_base/2) + c_rec_dom + c_rec_libre + c_rec_sa)*s_educ,2)
    c_unpac = round(c_base * unpac,2)
    c_isr_gr = round(((c_g_rep/2) * isr_grep),2)
    fo_atp_css = round(((fo_atp_base/2)+(fo_atp_grep/2)+fo_atp_rec_dom+fo_atp_rec_libre+fo_atp_rec_sa+fo_atp_rec_nac)*css_pa,2)
    fo_atp_seduc = round(((fo_atp_base/2)+fo_atp_rec_dom+fo_atp_rec_libre+fo_atp_rec_sa+fo_atp_rec_nac)*s_educ,2)
    fo_atp_unpac = round(fo_atp_base * unpac,2)
    fo_atp_isr_gr = round((fo_atp_grep/2)*isr_grep,2)
    fo_natp_css = round(((fo_atp_base/2)+fo_natp_rec_dom+fo_natp_rec_libre+fo_natp_rec_sa+fo_natp_rec_nac)*css_pa,2)
    fo_natp_seduc = round(((fo_atp_base/2)+fo_natp_rec_dom+fo_natp_rec_libre+fo_natp_rec_sa+fo_natp_rec_nac)*s_educ,2)
    fo_natp_unpac = round(fo_atp_base * unpac,2)
    fod_natp_unpac = round(fo_atp_base * unpac,2)
    fod_natp_isr_gr = round((fod_natp_grep/2)*isr_grep,2)
    fod_natp_seduc = round(((fo_atp_base/2)+fod_natp_rec_dom+fod_natp_rec_libre+fod_natp_rec_sa+fod_natp_rec_nac)*s_educ,2)
    fod_natp_css = round(((fo_atp_base/2)+(fod_natp_grep/2)+fod_natp_rec_dom+fod_natp_rec_libre+fod_natp_rec_sa+fod_natp_rec_nac)*css_pa,2)
    c_total_descuentos = round(c_css+c_seduc+c_isr_gr+c_unpac+c_isr,2)
    fo_atp_total_descuentos = round(fo_atp_css+fo_atp_seduc+fo_atp_isr_gr+fo_atp_unpac+fo_isr,2)
    fo_natp_total_deducciones = round(fo_natp_css+fo_natp_seduc+fo_natp_unpac+fo_isr,2)
    fod_natp_total_deducciones = round(fod_natp_css+fod_natp_seduc+fod_natp_isr_gr+fod_natp_unpac+fo_isr,2)
    c_neto = round(c_subt - c_total_descuentos,2)
    fod_natp_neto = round(fod_natp_subt - fod_natp_total_deducciones,2)
    fo_natp_neto = round(fo_natp_subt - fo_natp_total_deducciones,2)
    fo_atp_neto = round(fo_atp_subt - fo_atp_total_descuentos,2)


    if request.method == 'POST':
        logform = LogbookForm(request.POST)
        if logform.is_valid():
            cmp_id = logform.save(commit=False)
            cmp_id.cmp_id = request.user
            cmp_id.save()
            return redirect('logbook_calc') 
    context = {
        'c_isr' : c_isr,
        'fo_isr':fo_isr,
        'sel_month' : sel_month,
        'logform': logform,
        'logbook': logbook,
        'sum_block' : sum_block,
        'sum_sunday' : sum_sunday,
        'sum_holiday' : sum_holiday,
        'sum_libre' : sum_libre,
        'sum_sa' : sum_sa,
        'c_base' : c_base,
        'c_g_rep' : c_g_rep,
        'c_prima' : c_prima,
        'c_viatico' : c_viatico,
        'c_viatico_extra' : c_viatico_extra,
        'c_prima_extra' : c_prima_extra,
        'c_rata' : c_rata,
        'c_viatico_variable' : c_viatico_variable,
        'c_prima_variable' : c_prima_variable,
        'c_rec_dom' : c_rec_dom,
        'c_rec_libre' : c_rec_libre,
        'c_rec_sa' : c_rec_sa,
        'c_rec_nac' : c_rec_nac,
        'fo_atp_base' : fo_atp_base,
        'fo_atp_grep' : fo_atp_grep,
        'fo_atp_prima' : fo_atp_prima,
        'fo_atp_viatico' : fo_atp_viatico,
        'fo_atp_viatico_extra' : fo_atp_viatico_extra,
        'fo_atp_prima_extra' : fo_atp_prima_extra,
        'fod_natp_grep' : fod_natp_grep,
        'fo_atp_rata' : fo_atp_rata,
        'fod_natp_rata' : fod_natp_rata,
        'fo_natp_rata' : fo_natp_rata,
        'fod_natp_rec_dom' : fod_natp_rec_dom,
        'fo_atp_rec_dom' : fo_atp_rec_dom,
        'block_extra' : block_extra,
        'fo_viatico_extra' : fo_viatico_extra,
        'fo_prima_extra' : fo_prima_extra,
        'fod_natp_rec_libre' : fod_natp_rec_libre,
        'fod_natp_rec_sa' : fod_natp_rec_sa,
        'fod_natp_rec_nac' : fod_natp_rec_nac,
        'fo_natp_rec_dom' : fo_natp_rec_dom,
        'fo_natp_rec_libre' : fo_natp_rec_libre,
        'fo_natp_rec_sa' : fo_natp_rec_sa,
        'fo_natp_rec_nac' : fo_natp_rec_nac,
        'fo_atp_rec_libre' : fo_atp_rec_libre,
        'fo_atp_rec_sa' : fo_atp_rec_sa,
        'fo_atp_rec_nac' : fo_atp_rec_nac,
        'fod_natp_subt' : fod_natp_subt,
        'fo_natp_subt' : fo_natp_subt,
        'fo_atp_subt' : fo_atp_subt,
        'c_subt' : c_subt,
        'c_css' : c_css,
        'c_seduc' : c_seduc,
        'c_unpac' : c_unpac,
        'c_isr_gr' : c_isr_gr,
        'fo_atp_css' : fo_atp_css,
        'fo_atp_seduc' :fo_atp_seduc,
        'fo_atp_unpac' : fo_atp_unpac,
        'fo_atp_isr_gr' : fo_atp_isr_gr,
        'fo_natp_css' : fo_natp_css,
        'fo_natp_seduc' : fo_natp_seduc,
        'fo_natp_unpac' : fo_natp_unpac,
        'fod_natp_css' : fod_natp_css,
        'fod_natp_seduc' : fod_natp_seduc,
        'fod_natp_isr_gr' : fod_natp_isr_gr,
        'fod_natp_unpac' : fod_natp_unpac,
        'c_total_descuentos' : c_total_descuentos,
        'fo_atp_total_descuentos' : fo_atp_total_descuentos,
        'fo_natp_total_deducciones' : fo_natp_total_deducciones,
        'fod_natp_total_deducciones' : fod_natp_total_deducciones,
        'c_neto' : c_neto,
        'fod_natp_neto' : fod_natp_neto,
        'fo_natp_neto': fo_natp_neto,
        'fo_atp_neto' : fo_atp_neto,
        'today_is' : today_is
    }
    return render(request,'main/logbook_calc_Reserve.html', context)

#Delete Entry
def delete_entry(request, entry_id):
    delete_entry = Logbook.objects.get(pk=entry_id)
    delete_entry.delete()
    messages.error(request,'Entry DELETED!')
    return redirect('logbook_calc')

#User Profile
@login_required(login_url='login')
def userprofile(request,pk):
    user = User.objects.get(id=pk)
    user2 = request.user
    form = UpdateUserForm(instance=user2)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user2)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Updated Successfully')
            redirect('profile',pk=user.id)
        else:
            form.errors
            messages.error(request,'Error in update, Please verify your profile')
    return render(request,'main/user_profile.html', {'form': form})

# Verificar esto    
@login_required(login_url='login')
def RawLogbook(request):
    today_month = datetime.today().month
    current_month = calendar.month_name[int(today_month)]
    prev_month = today_month - 1
    if prev_month <= 0:
        current_month_minus1_int = 12 - prev_month
    else:
        current_month_minus1_int = prev_month
    current_month_minus1 = calendar.month_name[int(current_month_minus1_int)]
    if prev_month <= 0:
        current_month_minus2_int = 12 - prev_month
    else:
        current_month_minus2_int = prev_month
    current_month_minus2 = calendar.month_name[int(current_month_minus2_int)-2]
    raw_logbook = Logbook.objects.filter(cmp_id=request.user,date__month=today_month).order_by('date')
    raw_logbook_1 = Logbook.objects.filter(cmp_id=request.user,date__month=current_month_minus1_int).order_by('date')
    raw_logbook_2 = Logbook.objects.filter(cmp_id=request.user,date__month=current_month_minus2_int).order_by('date')

    context = {'raw_logbook' : raw_logbook,
    'current_month' : current_month,
    'current_month_minus1':current_month_minus1,
    'current_month_minus2':current_month_minus2,
    'raw_logbook_1' : raw_logbook_1,
    'raw_logbook_2' : raw_logbook_2
    }
    return render(request, 'main/logbook.html', context)




def ContactUs(request):
    return render(request, 'main/contact_us.html')


def HelpCenter(request):
    return render(request, 'main/help_center.html')

def OnDev(request):
    return render(request, 'main/OnDev.html')
