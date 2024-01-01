from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class PilotRank(models.Model):
    pilot_position = models.CharField(max_length=10)

    def __str__(self):
        return self.pilot_position

class User(AbstractUser):
    cmp_id = models.CharField(unique=True, max_length=20, null=True)
    username = models.CharField(max_length=20)
    email = models.EmailField(null=True)
    position = models.ForeignKey(PilotRank,on_delete=models.CASCADE,max_length=20,null=True)
    custom_disc_1 = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    custom_disc_1_name =models.CharField(max_length=250,default='Descuento 1')
    custom_disc_2 = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    custom_disc_2_name =models.CharField(max_length=250,default='Descuento 2')
    custom_disc_3 = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    custom_disc_3_name =models.CharField(max_length=250,default='Descuento 3')
    custom_disc_4 = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    custom_disc_4_name =models.CharField(max_length=250,default='Descuento 5')
    custom_disc_5 = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    custom_disc_5_name =models.CharField(max_length=250,default='Descuento 5')

    USERNAME_FIELD  =   'cmp_id'
    REQUIRED_FIELDS =   ['username']

    def __str__(self):
        return str(self.cmp_id)

# -- Create Model for Equip --
class Aircraft_Type(models.Model):
    aircraft_type = models.CharField(max_length=200)

    def __str__(self):
        return self.aircraft_type

class Users(models.Model):
    user = models.CharField(max_length=200, blank=False)
    name = models.CharField(max_length=200, null=True, blank=False)
    lastname = models.CharField(max_length=200, null=True, blank=False)
    cm_id = models.CharField(max_length=7, blank=False)
    mail = models.EmailField(max_length=200, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
        
# --LOGOBOOK MODEL--
    

class Logbook(models.Model):
    def default_zero():
        return "0"

    date = models.DateField()
    cmp_id = models.CharField(max_length=6, null=True)
    route = models.CharField(max_length=250)
    #TOTAL
    total_hrs_input = models.CharField(max_length=2, null=False)
    total_min_input = models.CharField(max_length=2, null=False)
    total_decimal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_flight_block = models.CharField(max_length=5, null=True, blank=True)
    #SUN
    sun_hrs_input = models.CharField(max_length=2, null=True, blank=True, default=default_zero)
    sun_min_input = models.CharField(max_length=2, null=True, blank=True, default=default_zero)
    total_sun_block = models.CharField(max_length=5, null=True, blank=True)
    sun_decimal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #HOLYDAY
    holiday_hrs_input = models.CharField(max_length=2, null=True, blank=True, default=default_zero)
    holiday_min_input = models.CharField(max_length=2, null=True, blank=True, default=default_zero)
    total_holiday_block = models.CharField(max_length=5, null=True, blank=True)
    holiday_decimal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #L
    libre_hrs_input = models.CharField(max_length=2, null=True, blank=True, default=default_zero)
    libre_min_input = models.CharField(max_length=2, null=True, blank=True, default=default_zero)
    total_libre_block = models.CharField(max_length=5, null=True, blank=True)
    libre_decimal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #SA
    sa_hrs_input = models.CharField(max_length=2, null=True, blank=True, default=default_zero)
    sa_min_input = models.CharField(max_length=2, null=True, blank=True, default=default_zero)
    total_sa_block = models.CharField(max_length=5, null=True, blank=True)
    sa_decimal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #REMARKS
    incentive = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarks = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


#RECUERDA: Limpiar el model antes de makemigrations!
        
    def caps_fm(self):
        xyz = self.route
        caps_from = xyz.upper()
        return caps_from

    #BLOCK_COMPUTED
    def get_computed_block(self):
        min_div = float(self.total_min_input) / 60
        result = min_div + float(self.total_hrs_input)
        return result
    
    def get_raw_time(self):
        raw_time_input = self.total_hrs_input + ':' + self.total_min_input
        return raw_time_input

    #SUN_COMPUTED
    def get_computed_sun(self):
        min_div = float(self.sun_min_input) / 60
        result = min_div + float(self.sun_hrs_input)
        return result
    
    def get_raw_time_sun(self):
        raw_time_input_sun = self.sun_hrs_input + ':' + self.sun_min_input
        return raw_time_input_sun
    
    #HOLYDAY_COMPUTED
    def get_computed_holiday(self):
        min_div = float(self.holiday_min_input) / 60
        result = min_div + float(self.holiday_hrs_input)
        return result
    
    def get_raw_time_holiday(self):
        raw_time_input_holiday = self.holiday_hrs_input + ':' + self.holiday_min_input
        return raw_time_input_holiday

    #LIBRE_COMPUTED
    def get_computed_libre(self):
        min_div = float(self.libre_min_input) / 60
        result = min_div + float(self.libre_hrs_input)
        return result
    
    def get_raw_time_libre(self):
        raw_time_input_libre = self.libre_hrs_input + ':' + self.libre_min_input
        return raw_time_input_libre

    #SA_COMPUTED
    def get_computed_sa(self):
        min_div = float(self.sa_min_input) / 60
        result = min_div + float(self.sa_hrs_input)
        return result
    
    def get_raw_time_sa(self):
        raw_time_input_sa = self.sa_hrs_input + ':' + self.sa_min_input
        return raw_time_input_sa
    

    def save(self, *args,**kwargs):
        self.total_decimal = self.get_computed_block()
        self.total_flight_block = self.get_raw_time()
        self.sun_decimal = self.get_computed_sun()
        self.total_sun_block = self.get_raw_time_sun()
        self.holiday_decimal = self.get_computed_holiday()
        self.total_holiday_block = self.get_raw_time_holiday()
        self.libre_decimal = self.get_computed_libre()
        self.total_libre_block = self.get_raw_time_libre()
        self.sa_decimal = self.get_computed_sa()
        self.total_sa_block = self.get_raw_time_sa()
        self.route = self.caps_fm()
        super(Logbook, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.cmp_id)
    
class Airports(models.Model):
    oaci_id = models.CharField(max_length=250)
    iata_id = models.CharField(max_length=250)
    airport_name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.iata_id)