# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Banks(models.Model):
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    bank_name = models.TextField(db_column='Bank_Name', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Banks'


class Clinics(models.Model):
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    clinic_name = models.TextField(db_column='Clinic_Name', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Clinics'


class Clubs(models.Model):
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    club_name = models.TextField(db_column='Club_Name', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Clubs'


class CommentsClient(models.Model):
    id = models.IntegerField(primary_key=True)
    categorie = models.TextField(db_column='Categorie', blank=True, null=True)  # Field name made lowercase.
    note = models.TextField(db_column='Note', blank=True, null=True)  # Field name made lowercase.
    hotel = models.ForeignKey('HotelInfo', models.DO_NOTHING, db_column='Hotel_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comments_Client'


class EnvironsHotel(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.TextField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    details = models.TextField(db_column='Details', blank=True, null=True)  # Field name made lowercase.
    hotel = models.ForeignKey('HotelInfo', models.DO_NOTHING, db_column='Hotel_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Environs_Hotel'


class EquipementHotel(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.TextField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    details = models.TextField(db_column='Details', blank=True, null=True)  # Field name made lowercase.
    hotel = models.ForeignKey('HotelInfo', models.DO_NOTHING, db_column='Hotel_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Equipement_Hotel'


class HotelInfo(models.Model):
    hotel_id = models.IntegerField(db_column='Hotel_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    city = models.TextField(db_column='City', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    type = models.TextField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    images = models.TextField(db_column='Images', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    stars = models.TextField(db_column='Stars', blank=True, null=True)  # Field name made lowercase.
    sustainable = models.TextField(db_column='Sustainable', blank=True, null=True)  # Field name made lowercase.
    restaurants = models.TextField(db_column='Restaurants', blank=True, null=True)  # Field name made lowercase.
    restaurants_more_details = models.TextField(db_column='Restaurants_More_details', blank=True, null=True)  # Field name made lowercase.
    point_fort = models.TextField(db_column='Point_Fort', blank=True, null=True)  # Field name made lowercase.
    comment_rating = models.TextField(db_column='Comment_Rating', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Hotel_Info'


class InfoHotelsDetails(models.Model):
    hotel_id = models.IntegerField(db_column='Hotel_ID', primary_key=True)  # Field name made lowercase.
    hotel_name = models.TextField(db_column='Hotel_Name', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    phone = models.TextField(db_column='Phone', blank=True, null=True)  # Field name made lowercase.
    fax = models.TextField(db_column='Fax', blank=True, null=True)  # Field name made lowercase.
    web = models.TextField(db_column='Web', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    covid_19_policies = models.TextField(db_column='COVID_19_Policies', blank=True, null=True)  # Field name made lowercase.
    year_built = models.CharField(db_column='Year_Built', max_length=4, blank=True, null=True)  # Field name made lowercase.
    check_in_time = models.TimeField(db_column='Check_in_time', blank=True, null=True)  # Field name made lowercase.
    check_out_time = models.TimeField(db_column='Check_out_Time', blank=True, null=True)  # Field name made lowercase.
    number_of_floors = models.IntegerField(db_column='Number_of_Floors', blank=True, null=True)  # Field name made lowercase.
    total_number_of_rooms = models.IntegerField(db_column='Total_Number_of_Rooms', blank=True, null=True)  # Field name made lowercase.
    chain = models.TextField(db_column='Chain', blank=True, null=True)  # Field name made lowercase.
    chain_website = models.TextField(db_column='Chain_Website', blank=True, null=True)  # Field name made lowercase.
    total_number_of_meeting_rooms = models.IntegerField(db_column='Total_number_of_meeting_rooms', blank=True, null=True)  # Field name made lowercase.
    total_event_space = models.TextField(db_column='Total_event_space', blank=True, null=True)  # Field name made lowercase.
    total_meeting_room_capacity = models.TextField(db_column='Total_meeting_room_capacity', blank=True, null=True)  # Field name made lowercase.
    meeting_facilities = models.TextField(db_column='Meeting_Facilities', blank=True, null=True)  # Field name made lowercase.
    guest_services = models.TextField(db_column='Guest_Services', blank=True, null=True)  # Field name made lowercase.
    security = models.TextField(db_column='Security', blank=True, null=True)  # Field name made lowercase.
    amenities = models.TextField(db_column='Amenities', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Info_Hotels_details'


class MeetingRooms(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    hotel = models.ForeignKey(InfoHotelsDetails, models.DO_NOTHING, db_column='Hotel_ID', blank=True, null=True)  # Field name made lowercase.
    nom = models.TextField(db_column='Nom', blank=True, null=True)  # Field name made lowercase.
    dimensions = models.TextField(db_column='Dimensions', blank=True, null=True)  # Field name made lowercase.
    area = models.TextField(db_column='Area', blank=True, null=True)  # Field name made lowercase.
    floor_number = models.TextField(db_column='Floor_Number', blank=True, null=True)  # Field name made lowercase.
    floor_cover = models.TextField(db_column='Floor_Cover', blank=True, null=True)  # Field name made lowercase.
    portable_walls = models.TextField(db_column='Portable_Walls', blank=True, null=True)  # Field name made lowercase.
    auditorium = models.IntegerField(db_column='Auditorium', blank=True, null=True)  # Field name made lowercase.
    classroom = models.IntegerField(db_column='Classroom', blank=True, null=True)  # Field name made lowercase.
    u_shape = models.IntegerField(db_column='U_Shape', blank=True, null=True)  # Field name made lowercase.
    reception = models.IntegerField(db_column='Reception', blank=True, null=True)  # Field name made lowercase.
    banquet = models.IntegerField(db_column='Banquet', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Meeting_Rooms'


class Restaut(models.Model):
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    restaut_name = models.TextField(db_column='Restaut_Name', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Restaut'



class Parkdata(models.Model):
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    nom = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parkdata'
