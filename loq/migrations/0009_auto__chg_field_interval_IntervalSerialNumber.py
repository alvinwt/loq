# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Interval.IntervalSerialNumber'
        db.alter_column(u'loq_interval', 'IntervalSerialNumber', self.gf('django.db.models.fields.SlugField')(max_length=45, null=True))

    def backwards(self, orm):

        # Changing field 'Interval.IntervalSerialNumber'
        db.alter_column(u'loq_interval', 'IntervalSerialNumber', self.gf('django.db.models.fields.SlugField')(default='', max_length=45))

    models = {
        u'loq.genome_build': {
            'Meta': {'object_name': 'Genome_Build'},
            'genome_build_id': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'loq.interval': {
            'Annotations': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'IntervalSerialNumber': ('django.db.models.fields.SlugField', [], {'max_length': '45', 'null': 'True'}),
            'IntervalSize': ('django.db.models.fields.IntegerField', [], {'max_length': '45', 'blank': 'True'}),
            'Link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'Meta': {'unique_together': "(('chr', 'start', 'stop'),)", 'object_name': 'Interval'},
            'NeatName': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '100'}),
            'Structure': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Tags': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            'chr': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.IntegerField', [], {'max_length': '15'}),
            'stop': ('django.db.models.fields.IntegerField', [], {'max_length': '15'})
        },
        u'loq.library': {
            'Meta': {'ordering': "['library_id']", 'object_name': 'Library'},
            'allele': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'five_prime_adapter_sequence': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'library_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'}),
            'multiplex_barcode_sequence': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'organism': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'source_org': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'source_person': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'strain': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'three_prime_adapter_sequence': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'tissue': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'})
        },
        u'loq.library_sequencing_run': {
            'Meta': {'object_name': 'Library_Sequencing_Run'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'library_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loq.Library']"}),
            'seq_run_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loq.Sequencing_Run']"})
        },
        u'loq.read_alignment': {
            'AGO1IPoverTotalRNA': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '15'}),
            'Meta': {'object_name': 'Read_alignment'},
            'big2catrenormRPmirpre': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '15'}),
            'chr': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'genomic_hits': ('django.db.models.fields.IntegerField', [], {'max_length': '45'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lib': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'normReads': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'read_counts': ('django.db.models.fields.IntegerField', [], {'max_length': '45', 'null': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'start': ('django.db.models.fields.IntegerField', [], {'max_length': '45'}),
            'stop': ('django.db.models.fields.IntegerField', [], {'max_length': '45'}),
            'strand': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'structure': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'})
        },
        u'loq.sequencing_run': {
            'GSE': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'GSM': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'Meta': {'object_name': 'Sequencing_Run'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mirror_track_group': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'modENCODE_id': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'release_status': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'seq_run_id': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'sequencing_center': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        }
    }

    complete_apps = ['loq']