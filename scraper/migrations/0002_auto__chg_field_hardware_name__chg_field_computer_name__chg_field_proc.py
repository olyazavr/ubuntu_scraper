# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Hardware.name'
        db.alter_column(u'scraper_hardware', 'name', self.gf('django.db.models.fields.CharField')(max_length=500))

        # Changing field 'Computer.name'
        db.alter_column(u'scraper_computer', 'name', self.gf('django.db.models.fields.CharField')(max_length=500))

        # Changing field 'Processor.name'
        db.alter_column(u'scraper_processor', 'name', self.gf('django.db.models.fields.CharField')(max_length=500))

    def backwards(self, orm):

        # Changing field 'Hardware.name'
        db.alter_column(u'scraper_hardware', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Computer.name'
        db.alter_column(u'scraper_computer', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Processor.name'
        db.alter_column(u'scraper_processor', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        u'scraper.computer': {
            'Meta': {'object_name': 'Computer'},
            'certified': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'scraper.hardware': {
            'Meta': {'object_name': 'Hardware'},
            'computersIn': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['scraper.Computer']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'scraper.processor': {
            'Meta': {'object_name': 'Processor'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'graphics': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['scraper']