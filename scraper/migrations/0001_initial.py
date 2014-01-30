# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Computer'
        db.create_table(u'scraper_computer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('certified', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'scraper', ['Computer'])

        # Adding model 'Hardware'
        db.create_table(u'scraper_hardware', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'scraper', ['Hardware'])

        # Adding M2M table for field computersIn on 'Hardware'
        db.create_table(u'scraper_hardware_computersIn', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hardware', models.ForeignKey(orm[u'scraper.hardware'], null=False)),
            ('computer', models.ForeignKey(orm[u'scraper.computer'], null=False))
        ))
        db.create_unique(u'scraper_hardware_computersIn', ['hardware_id', 'computer_id'])

        # Adding model 'Processor'
        db.create_table(u'scraper_processor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('graphics', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'scraper', ['Processor'])


    def backwards(self, orm):
        # Deleting model 'Computer'
        db.delete_table(u'scraper_computer')

        # Deleting model 'Hardware'
        db.delete_table(u'scraper_hardware')

        # Removing M2M table for field computersIn on 'Hardware'
        db.delete_table('scraper_hardware_computersIn')

        # Deleting model 'Processor'
        db.delete_table(u'scraper_processor')


    models = {
        u'scraper.computer': {
            'Meta': {'object_name': 'Computer'},
            'certified': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'scraper.hardware': {
            'Meta': {'object_name': 'Hardware'},
            'computersIn': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['scraper.Computer']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'scraper.processor': {
            'Meta': {'object_name': 'Processor'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'graphics': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['scraper']