from django.db import models
from django.contrib.gis.db import models as geomodels
from django.utils.crypto import get_random_string
# Create your models here.

class Zone(geomodels.Model):
    point = geomodels.PointField(blank=True, null=True)
    objects = geomodels.GeoManager() 

    def __unicode__(self):
        return 'Zone %s' % self.id

    class Meta:
        db_table = 'zones'
        verbose_name_plural = "zones"


class Location(geomodels.Model):
    point = geomodels.PointField(blank=True, null=True)
    objects = geomodels.GeoManager()

    def __unicode__(self):
        return 'Location %s' % self.id

    class Meta:
        db_table = 'location'
        verbose_name_plural = "locations"


class Bikes(models.Model):
    location = models.ForeignKey(Location, blank=True, null=True)
    free = models.BooleanField(default=True)
    damaged = models.BooleanField(default=False)
    distance = models.IntegerField(default=0)

    def __unicode__(self):
        return 'Bike %s' % self.id

    class Meta:
        db_table = 'bikes'
        verbose_name_plural = "bikes"


class Users(models.Model):
    uid = models.CharField(max_length=64, blank=False, null=False, default=get_random_string(64))
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    distance = models.IntegerField(default=0)
    location = models.ForeignKey(Location, blank=True, null=True)
    bike = models.ForeignKey(Bikes, blank=True, null=True)

    def __unicode__(self):
        return 'User %s' % self.id
    
    def save(self, *args, **kwargs):
        ''' Update uuid '''
        user_uuid = get_random_string(64)
        if not self.id:
            self.uid = user_uuid
        return super(Users, self).save(*args, **kwargs)

    class Meta:
        db_table = 'users'
        verbose_name_plural = "users"

