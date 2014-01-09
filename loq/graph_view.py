from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.shortcuts import render
import pandas as pd
import numpy as np
from django.db.models import Count, Sum
import matplotlib.pyplot as plt
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from loq.models import Interval ,Read_alignment, Library
from loq.forms import GraphForm
from django.contrib import messages
from django.core.context_processors import csrf
from django.forms import ValidationError
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.db.models import Count, Sum
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
sns.set(style='whitegrid',palette=["#000000", "#E69F00", "#56B4E9", "#009E73", "#8C1515", "#D55E00", "#CC79A7"],context='talk')

def Graph_Form(request):
    errors = []
    if request.user.is_authenticated():
        if request.method == 'POST':
            if not request.POST.get('mirName',''):
                errors.append("Enter a miRNA name")
            form = GraphForm(request.POST)
            if form.is_valid():
                name= form.cleaned_data['mirName']
                libraries = form.cleaned_data['Library']
                chart_type = form.cleaned_data['Chart']
                normal = form.cleaned_data['Normal']
                try:
                    interval_object = Interval.objects.select_related().get(mirName__icontains=name)
                    read_object= interval_object.read_alignment_set.filter(lib__in=libraries).order_by('lib')
                    len_count =read_object.values('read_length','lib','read_counts','intervalName__sum_read_counts','normReads').annotate(Count('read_length')).order_by('read_length')
                    lib_total_count =read_object.values('lib').annotate(Sum('read_counts'))
                    length=[]
                    for i in len_count:
                        length.append(int(i['read_length']))
                        lengths_reads = sorted(set(length))
                
                    df = pd.DataFrame(index=lengths_reads, columns=libraries)
                    df = df.fillna(0).convert_objects()
                    d= {}
                
                    for j in lib_total_count:
                        d[j['lib']] = j['read_counts__sum']
                        
                    for i in len_count:
                        lb=i['lib']
                        lh=i['read_length']
                        if normal == 'dist_rpm':
                            data = int(i['read_length__count']*i['normReads'])
                            title = 'Reads per million'
                        elif normal == 'dist_read_counts':
                            data = int(i['read_length__count']*i['read_counts'])
                            title = 'Reads Counts'
                        else: 
                            data = int((100*i['read_length__count']*i['read_counts'])/d[i['lib']])
                            title ='Read counts per miRNA mapped'
                        df[lb][lh] += data
          
                    fig= plt.figure()
                    ax = fig.add_subplot(111)
                    df.plot(ax=ax, kind=chart_type,figsize=(10,8),subplots=False,)
                    plt.title('Read Length Distribution of '+ str(interval_object.mirName))
                    plt.xlabel('Length of Read')
                    plt.grid(True)
                    plt.ylabel(title)
                    canvas = FigureCanvas(fig)
                    response = HttpResponse(mimetype='image/jpg')
                    canvas.print_png(response)
                    return response
                # return HttpResponseRedirect(reverse('IntervalDetailView', kwargs={'pk': interval_object.pk}))
                except (MultipleObjectsReturned), e :
                    return HttpResponse("Please provide a specific query. Your search returned more than one result.")
            
                except ObjectDoesNotExist:
                    return HttpResponse("Please check your query, the miRNA does not exist in the database.")          
        else:
            form = GraphForm()
            return render(request,'loq/graph_filter.html',{'form':form,'errors':errors })
    else:
        return HttpResponseRedirect('/login/')

# class Graph_Form(View,ModelFormMixin):
#     model = Interval
#     fields = ['id']
#     form_class= GraphForm

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated():
#             return HttpResponseForbidden()
#         self.object = self.get_object() 
#         return super(Graph_Form, self).post(request, *args, **kwargs)

# def Graph_Filter(request):
#     if request.POST:
#         form=GraphForm(request.POST)
#         if form.is_valid():
#             url = '/'+ str(form.cleaned_data['id']) +'/interval/'
#             return HttpResponseRedirect(url)

# class Graph_Form(FormView):
#     model = Interval
#     form_class = GraphForm
#     template_name ='loq/graph_filter.html'
   

#     def form_valid(self,form):
#         if form.is_valid():
#             new_object = form.save()
#         return super(Graph_Form,self).form_valid(form)

#     def get_success_url(self):
#         return reverse('IntervalDetailView', kwargs={'pk': new_object.pk})
    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(object=id)
    #     return self.render_to_response(context)
     
    # def get_success_url(self):
    #     # Redirect to previous url
    #     return self.request.META.get('HTTP_REFERER', None)
            
    # def get_form_kwargs(self):
    #     kwargs = super(Graph_Filter, self).get_form_kwargs()
    #     kwargs['id'] = self.request.id
    #     return kwargs

    
    # def post(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated():
    #         return HttpResponseForbidden()
    #     self.object = self.get_object() 
    #     return super(Graph_Filter, self).post(request, *args, **kwargs)
  

    # def success_url(self):
    #     b = form.cleaned_data['IntervalSerialNumber']
    #     return reverse('IntervalDetailView')

    
    #     else:
    #         print 'error'
    # def form_invalid(self,form):
    #     print "Your submission has not been saved. Try again."
    #     return super(Graph_Filter, self).form_invalid(form)    
