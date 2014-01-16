### This is a model file for the Small RNA Biogenesis database. This will have the database modelling details. Whether blank=True, Null=True, ManyToManyField or ForeignKeys can be deliminated. 

from django.db import models
from django.db.models import Avg, F
from django.forms import ModelForm
from decimal import Decimal
from django.core.urlresolvers import reverse
import django_filters 

class Interval(models.Model):
    #mapped intervals and locations can be used to link to USCS genome browser
    chr= models.CharField(max_length=45)
    start= models.IntegerField(max_length=15)
    stop= models.IntegerField(max_length=15)
    mirName= models.CharField(max_length=40,default='',verbose_name='miRNA Name')
    NeatName= models.CharField(max_length=100,default='0', verbose_name='Neat Name')
    IntervalSize= models.IntegerField(max_length=45,blank=True,verbose_name='Interval Size' )
    IntervalSerialNumber = models.IntegerField(max_length=45,verbose_name='Interval Id', null=True)
    Structure= models.CharField(max_length=200, blank=True)
    Annotations = models.TextField(max_length=1000,blank=True)
    Tags= models.TextField(max_length=100,blank=True, verbose_name='Comments')
    sum_read_counts = models.IntegerField(max_length=10000, null=True, verbose_name='Reads Mapped')
    sum_normReads = models.FloatField(null=True,verbose_name='Total Normalized Reads')
    mapped_strand = models.CharField(max_length=5, choices={('+','+'),('-','-')}, verbose_name='miRNA Strand')
    mid_point =models.IntegerField(max_length=45,blank=True)
    Link= models.URLField(max_length=200,blank=True)

    @property
    def interval (self):
        return '%s:%s,%s' %(self.chr,str(self.start+1),str(self.stop))

    class Meta:
        unique_together = ('chr','start','stop')
    
    def __unicode__(self):
        return u'%s:%s-%s' %(self.chr,str(self.start),str(self.stop))

    def get_absolute_url(self):
        return reverse('IntervalDetailView', kwargs={'pk': self.object.pk})
      
class Library(models.Model):
    #library contains information about each library, called upon when needed for comparison.
    library_id = models.CharField(max_length=16,primary_key=True)
    description = models.CharField(max_length=255, blank=True)
    organism = models.CharField(max_length=45, blank=True)
    strain = models.CharField(max_length=45, blank=True)
    allele = models.CharField(max_length=45, blank=True)
    tissue = models.CharField(max_length=128, blank=True)
    target = models.CharField(max_length=45, blank=True)
    type =  models.CharField(max_length=45, blank=True)
    total_mapped =models.BigIntegerField(max_length=100,blank=True)
    resolution =  models.CharField(max_length=45, blank=True)
    source_org =  models.CharField(max_length=45, blank=True)
    source_person = models.CharField(max_length=45, blank=True)
    five_prime_adapter_sequence = models.CharField(max_length=128, blank=True)
    three_prime_adapter_sequence = models.CharField(max_length=128, blank=True)
    multiplex_barcode_sequence =  models.CharField(max_length=45, blank=True)
    notes = models.TextField(max_length=500, blank=True)
    
    def __unicode__(self):
         return self.library_id
     
    class Meta:
         ordering = ['library_id']
         
class Sequencing_Run(models.Model):
    seq_run_id = models.CharField(max_length=16)
    sequencing_center = models.CharField(max_length=45)
    release_status = models.CharField(max_length=45, blank=True)
    GSM = models.CharField(max_length=45, blank=True)
    GSE = models.CharField(max_length=45, blank=True)
    modENCODE_id = models.CharField(max_length=45, blank=True)
    mirror_track_group = models.CharField(max_length=45, blank=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.seq_run_id, self.sequencing_center)
    
class Library_Sequencing_Run(models.Model):
    library_id= models.ForeignKey(Library)
    seq_run_id= models.ForeignKey(Sequencing_Run)
    def __unicode__(self):
        return u'%s %s' % (self.library_id, self.seq_run_id)

class Genome_Build(models.Model):
    genome_build_id = models.CharField(max_length=45)

    def __unicode__(self):
        return self.genome_build_id

class PlusManager(models.Manager):
    def get_queryset(self):
        return super(PlusManager,self).get_queryset().filter(strand='+')

    
class MinusManager(models.Manager):
    def get_queryset(self):
        return super(MinusManager,self).get_queryset().filter(strand='-')
        
class Graph_Manager(models.Manager):
    def get_graph(self):
        if int(self.start)- 20 < 0:
            start = self.start
        else:
            start = int(self.start) - 20

            graph_query = Read_alignment.objects.get_queryset().filter(start__lte=int(start),stop__gte= int(self.stop)+50)    
            return graph_query.values_list 
class IntNamed(models.Manager):
    def get_name(self):
        if self.strand == '+':
            IntNamed= self.chr + ':' + int(self.start) +1 + '-' +self.stop
        else:
            IntNamed = "minus"
            return IntNamed

class Read_alignment(models.Model):
    #library can be used as a foreign key to link libraries to read alignments
    lib = models.CharField(max_length=50,blank=True)
    library = models.ForeignKey(Library)
    sequence = models.CharField(max_length=150)
    rev_sequence= models.CharField(max_length=150,null=True)
    read_counts = models.IntegerField(max_length=45, null=True)
    genomic_hits = models.IntegerField(max_length=45)
    chr = models.CharField(max_length=45)
    start = models.IntegerField(max_length=45)
    stop = models.IntegerField(max_length=45)
    strand = models.CharField(max_length=5, choices={('+','+'),('-','-')})
    #big2catrenormRPmirpre = models.DecimalField(max_digits=19,decimal_places=15,null=True)
    #AGO1IPoverTotalRNA = models.DecimalField(max_digits=19,decimal_places=15,null=True)
    normReads =models.FloatField(null=True)
    intervalName = models.ForeignKey(Interval,null=True)
    structure= models.CharField(max_length=1000,blank=True)
    read_length = models.IntegerField(max_length=100,null=True)
    IntName= IntNamed()
    # IntName = models.ForeignKey(Interval,to_field='NeatName')
    objects = models.Manager()
    aligned_objects = Graph_Manager()
    minus = MinusManager()
    plus = PlusManager()

    
    #"V063V0632renormRPmirpreadd" to "V066V0662renormRPmirpreadd" =normreads with diff headings for each lib?
    #aligned_interval = models.ForeignKey(Interval)
    # seq_run_id =  models.ForeignKey(Sequencing_Run)
    # genome_build_id = models.ForeignKey(Genome_Build)
    
    def __unicode__(self):
        return u'%s %s %s' % (self.chr, self.start, self.stop)
    
    # (read_counts/ genomic_hits) per million mirPrecursor Reads
    # consider pickling, or using celery for reducing lag / processing time
    # think how to code this dynamically. not hard coding.
    
    #saving calculated figures to db can allow searching. but has to be done in shell. 
    def normRead(self):
        ### wtCS = Read_alignment.objects.filter(library__contains=lib)
        wtCS_mapped = int(86837856) / 10^6
        normalized_count = (Decimal(self.read_counts) / Decimal(self.genomic_hits)) / wtCS_mapped
        normalized = '%e' % (normalized_count)
        return normalized_count
    
    # def save(self, *args, **kwargs):
    #     a= self.normRead()
    #     super(Read_alignment,self).save(*args,**kwargs)
    #     self.normReads=a
    #     return self.normReads
        
class IntervalFilter(django_filters.FilterSet):

    # def __init__(self,*args,**kwargs):
    #     super(IntervalFilter,self).__init__(*args,**kwargs)
  
    df= django_filters
    start = df.RangeFilter()
    stop = df.RangeFilter()
    chr =df.CharFilter(lookup_type='icontains')
    # Tags =df.AllValuesFilter()
    mirName =df.CharFilter(lookup_type='icontains',label='miRNA Name')
    Annotations=df.AllValuesFilter()
    IntervalSerialNumber =df.NumberFilter(label='Id')
    NeatName = df.CharFilter(label='Genomic Location')
    class Meta:
        model = Interval
        fields = ['mirName','IntervalSerialNumber','chr','start','stop','Annotations','NeatName']
        #order_by = (('NeatName', 'Interval'),
        #            ('start','Start range'),
        #            ('stop','Stop Range'))

class AlignFilter(django_filters.FilterSet):
     df= django_filters
     start = df.RangeFilter()
     stop = df.RangeFilter()
     chr =df.AllValuesFilter()
     normReads = df.RangeFilter()
     # intervalName=df.AllValuesFilter()
     
     class Meta:
        model = Read_alignment
        fields = ['chr','strand','start','stop','read_counts','normReads',]
 
# class GraphFilter(ModelForm):
#     # start = df.NumberFilter(lookup_type='gte')
#     # stop = df.NumberFilter('lte')
#     # # Library =df.ModelMultipleChoiceFilter()
#     # chr =df.CharFilter(lookup_type='icontains')
#     # IntervalSerialNumber =df.NumberFilter(label='Id')
#     # mirName =df.CharFilter(lookup_type='icontains',label='miRNA Name')
#     class Meta:
#         model = Interval
#         fields = ['mirName','IntervalSerialNumber','chr','start','stop']      
