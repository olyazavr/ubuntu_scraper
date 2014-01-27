from django.db import models

class Computer(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=200)
    certified = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    ''' Get the brand from the first word of the name (lame, but looks nice)'''
    def brand(self):
        return self.name.split(" ")[0]
    brand.admin_order_field = 'name'

    ''' Convert flattened string of parts into list '''
    def splitParts(self):
        if self.parts:
            return self.parts.split(", ")
        return ''

class Hardware(models.Model):
    url = models.URLField(null=True)
    name = models.CharField(max_length=200)
    computersCertifiedIn = models.ManyToManyField(Computer, related_name='certifiedIn')
    computersEnabledIn = models.ManyToManyField(Computer, related_name='enabledIn')
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    ''' Is it certified in at least one computer; if not, is it enabled in at least
        one computer. Otherwise, it is unknown. '''
    def certified(self):
        if self.computersCertifiedIn:
            return "Certified"
        if self.computersEnabledIn:
            return "Enabled"
        return "Unknown"

    ''' Get the brand from the first word of the name (lame, but looks nice)'''
    def brand(self):
        return self.name.split(" ")[0]
    brand.admin_order_field = 'name'

    ''' Convert flattened string of computersCertifiedIn into list. Duplicate
        because Django views cannot pass arguments into methods. '''
    def splitCertComp(self):
        if self.computersCertifiedIn:
            return self.computersCertifiedIn.split(", ")
        return ''

    ''' Convert flattened string of computersEnabledIn into list. Duplicate
        because Django views cannot pass arguments into methods. '''
    def splitEnabComp(self):
        if self.computersEnabledIn:
            return self.computersEnabledIn.split(", ")
        return ''