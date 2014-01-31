from django.db import models

class Computer(models.Model):
    url = models.URLField(unique=True, max_length=500)
    name = models.CharField(max_length=500)
    certified = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Hardware(models.Model):
    url = models.URLField(null=True, max_length=500)
    name = models.CharField(max_length=500)
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
        

class Processor(models.Model):
    url = models.URLField(unique=True, max_length=500)
    name = models.CharField(max_length=500)
    codename = models.CharField(max_length=200)
    graphics = models.CharField(max_length=200, null=True)
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name