from django.db import models

class Computer(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=200)
    certified = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def brand(self):
        ''' Get the brand from the first word of the name (lame, but looks nice)'''

        return self.name.split(" ")[0]
    brand.admin_order_field = 'name'
    

class Hardware(models.Model):
    url = models.URLField(null=True)
    name = models.CharField(max_length=200)
    computersIn = models.ManyToManyField(Computer)
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
    
    def certified(self):
        ''' Is it certified in at least one computer; if not, is it enabled in at least
        one computer. Otherwise, it is unknown. '''

        if self.computersCertifiedIn():
            return "Certified"
        if self.computersEnabledIn():
            return "Enabled"
        return "Unknown"

    def computersCertifiedIn(self):
        ''' Returns the set of computers the part is in that are certified '''

        return self.computersIn.filter(certified='Certified')

    def computersEnabledIn(self):
        ''' Returns the set of computers the part is in that are enabled '''

        return self.computersIn.filter(certified='Enabled')

    def brand(self):
        ''' Get the brand from the first word of the name (lame, but looks nice)'''

        return self.name.split(" ")[0]
    brand.admin_order_field = 'name'


class Processor(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=200)
    codename = models.CharField(max_length=200)
    graphics = models.CharField(max_length=200, null=True)
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name