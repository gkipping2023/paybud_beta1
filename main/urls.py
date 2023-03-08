from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register_user/', views.registeruser, name='register'),
    path('', views.home, name='home'),
    path('logbook/', views.RawLogbook, name='logbook'),
    path('simple_calc/', views.simplecalc, name='simple_calc'),
    path('delete_entry/<entry_id>', views.delete_entry, name='delete_entry'),
    path('logbook_calculator/', views.logbook_calc, name='logbook_calc'),
    path('logbook_calculator_RESERVE/', views.logbook_calc_reserve, name='logbook_calc_reserve'),
    path('contact-us/', views.ContactUs, name='contact-us'),
    path('help/', views.HelpCenter, name='help-center'),
    path('on-development/', views.OnDev, name='on-development'),
]