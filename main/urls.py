from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('flexpay/login/', views.loginPage, name='login'),
    path('flexpay/logout/', views.logoutUser, name='logout'),
    path('flexpay/register_user/', views.registeruser, name='register'),
    path('flexpay/', views.home, name='home'),
    path('', views.index, name='index'),
    path('flexpay/simple_calc/', views.simplecalc, name='simple_calc'),
    path('flexpay/simple_calc_cap/', views.simplecalc, name='simple_calc_cap'), 
    path('flexpay/simple_calc_fo_atp/', views.simplecalc, name='simple_calc_fo_atp'),
    path('flexpay/simple_calc_fo_natp/', views.simplecalc, name='simple_calc_fo_natp'),
    path('flexpay/simple_calc_fod_natp/', views.simplecalc, name='simple_calc_fod_natp'),
    path('flexpay/delete_entry/<entry_id>', views.delete_entry, name='delete_entry'),
    path('flexpay/profile/<str:pk>/', views.userprofile, name='profile'),
    path('flexpay/logbook_calculator/', views.logbook_calc, name='logbook_calc'),
    path('flexpay/contact-us/', views.ContactUs, name='contact-us'),
    path('flexpay/help/', views.HelpCenter, name='help-center'),
    path('flexpay/on-development/', views.OnDev, name='on-development'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='main/password_reset_view.html'),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/password_confirm_view.html'),name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'),name='password_reset_complete'),
]