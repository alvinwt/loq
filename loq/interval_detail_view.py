from django.views.generic import DetailView
from .models import Read_alignment, Interval
from .forms import GraphForm
import os
from django_tables2 import RequestConfig, SingleTableMixin
import re
from Bio import SeqIO
from Bio.Seq import Seq
import numpy as np
import pandas as pd
import itertools
from django.contrib.auth.decorators import login_required
from tables import DetailTable
from django.utils.decorators import method_decorator
from django.db.models import Count
    
class IntervalDetailView(SingleTableMixin,DetailView):
    model= Interval
    table_class = DetailTable
    context_table_name = 'interval_detail'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IntervalDetailView,self).dispatch(*args, **kwargs)
   
    def get_table_data (self):
        table_data= Read_alignment.objects.filter(intervalName=self.object)
        return table_data
    
    def get_seq(self):
        stt = self.object.start 
        stp = self.object.stop
        #still hardcoded! needs to be static*

        chrom = str(self.object.chr).replace('chr','')
        fasta_file= os.getcwd() + '/static/fasta/dmel-' + chrom+ '-chromosome-r5.50.fasta'

        for seq_record in SeqIO.parse(fasta_file,'fasta'):
            seq = seq_record.seq
        if self.object.mapped_strand == "+":
            seqInterval = str(seq[stt:stp])
        else:
            seqInterval = str(seq[stt:stp].reverse_complement())
        return seqInterval

    
            # rev_seq = seq_record.seq.reverse_complement()
            # if self.object.strand == '+':
               
            # else:
    
            
    def get_msa(self):
        self = self.object
        read_list=Read_alignment.objects.filter(intervalName=self,strand=self.mapped_strand).order_by('lib').select_related().order_by('start')
        count_seq=  read_list.values('sequence','start','stop').annotate(Count('sequence'))
        all_libs = read_list.values('lib').annotate(Count('lib'))
        allseqs =[]
        string ="\n\n"
        libs = []
        
        for i in count_seq:
            allseqs.append(i['sequence'])

  
        for i in all_libs:
            libs.append(i['lib'])
        libs = sorted(libs)
        df = pd.DataFrame(index=allseqs,columns =libs,dtype='float64')
        
        for i in read_list:
            df[i.lib][i.sequence] ='%.2f' % i.normReads

            # df = df.sort_index(ascending =False) 
        counts = df.to_string(index=None, na_rep ='',sparsify=True)

        for j in count_seq:
            if self.mapped_strand == '+':
                reads = '%s\n' % j['sequence'] 
                spaces = int(j['start'])-int(self.start)            
                if spaces >= 1:
                    string += spaces * ' ' + reads 
                else:
                    string += reads
            else:
                reads = '%s\n' % j['sequence']   
                spaces = int(self.stop)-int(j['stop'])
                if spaces >= 1:
                    string += spaces * ' ' + reads 
                else:
                    string += reads   
        return {'string':string, 'counts': counts}


    
        # # read_list = Read_alignment.objects.filter(chr= self.chr, start__gte= self.start , stop__lte=self.stop)
        # read_list=Read_alignment.objects.filter(intervalName=self,strand=self.mapped_strand).order_by('lib')
        # string =""
        # if self.mapped_strand == '+':
        #     for i in read_list:
        #         reads = '%s\n' % (i.sequence)
        #         spaces = int(i.start)-int(self.start)
        #         if spaces >= 1:
        #             string += spaces * ' ' + reads 
        #         else:
        #             string += reads
        # else:
        #     for i in read_list:
        #         reads = '%s\n' % (i.sequence)   
        #         spaces = int(self.stop)-int(i.stop)
        #         if spaces >= 1:
        #             string += spaces * ' ' + reads 
        #         else:
        #             string += reads 
       

    # def get_graph(self):
    #     self=self.object
    #     reads= Read_alignment.objects.filter(intervalName=self)
    #     cord = []
    #     data =[]
    #     index = []
    #     for i in reads:
    #         index.append(i.id)
    #         cord.append(i.start)
    #         cord.append(i.stop)
    #         ac =[int(i.start-self.start)*str(0),int(i.stop-i.start) *str(i.read_counts),int(self.stop-i.stop)*str(0)]
    #         data.append(list("".join(ac)))
    #     cords = range(self.start,self.stop)
    #     matrix = []
    #     for i in data:
    #         i=map(int,i)
    #         matrix.append(i)
    #     frame = pd.DataFrame(matrix,columns=cords, index=index)
    #     pile= frame.values.sum(axis=0)
    #     graph_list=[]
    #     #graph_list.insert(0,['Position', 'Counts'])
    #     for i in range(0,len(cords)):
    #         #cord = "'" + str(cords[i]) +"'"
    #         graph_list.append([str(cords[i]), pile[i]])
    #     return graph_list
    
    # def get_graph1(self):
    #     self=self.object
    #     reads= Read_alignment.objects.filter(intervalName=self)
    #     #print self.start 
    #     ### Draw the matrix
    #     table = {}
    #     list = []
    #     for i in range(self.start-1,self.stop+1):
    #         table[i]=int(0)
    #     for i in reads:
    #         row = [i.start, i.stop, i.normReads]
    #         for j in range(row[0],row[1]):
    #             try:
    #                 if j in table:
    #                     table[j] = table[j] + row[2]
    #             except:
    #                 print "index not found"

    #     for key, value in table.iteritems():
    #         temp = [key,int(value)]
    #         list.append(temp)
    #     list= sorted(list)
    #     for i in list:
    #         i[0]=str(i[0])
    #     return list
        
    def get_graph2(self):
        self=self.object
        reads= Read_alignment.objects.filter(intervalName=self,strand=self.mapped_strand).order_by('lib')
        libs = ['D005', 'D006','D007','D008','D009', 'D010']
        cords = np.arange(self.start-1,self.stop+1)
        
        df = pd.DataFrame(index=cords, columns=libs)
        df = df.fillna(0)
        for i in reads:
            for j in range(i.start,i.stop):
                df[i.lib][j] += i.normReads

        a= np.array(df)
        w = np.reshape(cords,(len(cords),-1))
        list = np.concatenate((w,a),axis=1)
        if self.mapped_strand == "-":
            list = np.flipud(list)
        else: 
            pass
        list = list.tolist()
        libs.insert(0,"Coordinates")
        list.insert(0,libs)
              
            #first_row.insert(0,'Coordinates')
            #list = list.insert(0,first_row)

        for i in list:
            i[0] =str(i[0])
        return list
        #first_row.append(str(i))
        #list = list.insert(0,first_row)        


    # def get_read_counts(self):
    #     self= self.object
    #     reads=Read_alignment.objects.filter(intervalName=self)
    #     count =""
    #     for i in reads:
    #         count += str(i.normReads)+' '+ str(i.lib) + "\n"  
    #     return count

    # def get_libname(self):
    #     self= self.object
    #     reads=Read_alignment.objects.filter(intervalName=self.NeatName)
    #     lib =""
    #     for i in reads:
    #         lib += str(i.read_counts)+"\n"  
    #     return lib
 

    def get_context_data(self, **kwargs):
        context = super(IntervalDetailView,self).get_context_data(**kwargs)
        context['seq'] = self.get_seq()
        context['msa'] = self.get_msa()['string']
        context['graph']= self.get_graph2()
        context['counts']=self.get_msa()['counts']
        context['form']= GraphForm
        # context['lib'] = self.get_libname()
        return context
    
