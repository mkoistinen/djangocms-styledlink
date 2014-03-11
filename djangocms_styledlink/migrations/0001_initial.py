# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StyledLinkStyle'
        db.create_table(u'djangocms_styledlink_styledlinkstyle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('link_class', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
        ))
        db.send_create_signal(u'djangocms_styledlink', ['StyledLinkStyle'])

        # Adding model 'StyledLink'
        db.create_table(u'cmsplugin_styledlink', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('int_destination_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('int_destination_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('page_destination', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('ext_destination', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('ext_follow', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('mailto', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'djangocms_styledlink', ['StyledLink'])

        # Adding M2M table for field styles on 'StyledLink'
        db.create_table(u'djangocms_styledlink_styledlink_styles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('styledlink', models.ForeignKey(orm[u'djangocms_styledlink.styledlink'], null=False)),
            ('styledlinkstyle', models.ForeignKey(orm[u'djangocms_styledlink.styledlinkstyle'], null=False))
        ))
        db.create_unique(u'djangocms_styledlink_styledlink_styles', ['styledlink_id', 'styledlinkstyle_id'])


    def backwards(self, orm):
        # Deleting model 'StyledLinkStyle'
        db.delete_table(u'djangocms_styledlink_styledlinkstyle')

        # Deleting model 'StyledLink'
        db.delete_table(u'cmsplugin_styledlink')

        # Removing M2M table for field styles on 'StyledLink'
        db.delete_table('djangocms_styledlink_styledlink_styles')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'djangocms_styledlink.styledlink': {
            'Meta': {'object_name': 'StyledLink', 'db_table': "u'cmsplugin_styledlink'", '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'ext_destination': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'ext_follow': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'int_destination_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'int_destination_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'mailto': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'page_destination': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'styles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'styled_link_style'", 'default': '1', 'to': u"orm['djangocms_styledlink.StyledLinkStyle']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        u'djangocms_styledlink.styledlinkstyle': {
            'Meta': {'object_name': 'StyledLinkStyle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'link_class': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        }
    }

    complete_apps = ['djangocms_styledlink']