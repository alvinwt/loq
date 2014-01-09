from django.forms import ModelForm
from srb.models import Interval

class MyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)
        self.fields['chr'].min_length= 1
    class Meta:
        model = Interval
        fields = ('chr','start','stop','NeatName','IntervalSerialNumber','Tags','Annotations')
