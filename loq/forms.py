from django import forms

class GraphForm(forms.Form):
    mirName = forms.CharField(max_length=100,label='miRNA Name',help_text="You can exclude 'dme-mir', but do provide a specific name e.g. 307a.")
    Library = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, choices=[('D005','D005'),('D006','D006'),('D007','D007'),('D008','D008'),('D009','D009'),('D010','D010')])
    Chart= forms.ChoiceField(required=True, label= "Chart type", choices=[('bar','Bar'),('line','Line'),('barh','Horizontal Bar')])
    Normal= forms.ChoiceField(required=True, label= "Normalization", choices=[('dist_read_counts','Raw Read Count'),('dist_rpm','Reads Per Million'),('dist_percent_read_counts','Percentage miRNA Mapped')])
     
    # def create_graph(self,form):
    #     if form.is_valid():
    #         pk = self.cleaned_data.get('id')
    #         selected_interval = Interval.objects.get(id=pk).values('chr','start','stop')
    #         pass
        #return pk
    #     object = Interval.objects.select_related().get(chr=self.chr,start=self.start,stop=self.stop,mirName=self.mirName)
    #     object= object.values('mirName','read_alignment__read_length','read_alignment__read-counts')
    #     return object 
