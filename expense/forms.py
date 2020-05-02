from django import forms

from .models import Income,Data,Category,Sub_Category

class CreateIncome(forms.ModelForm):
    class Meta:
        model = Income
        fields= [
            "name",
            "amt",
            "recursive",
            "pay_type",
        ]
class PostForm(forms.ModelForm):
    class Meta:
        model = Data
        fields= [
            "sub_category",
            "spent",
            "recursive",
            "pay_type",
        ]
class CreateCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields =[
            "name",
            "budget",
        ]
class StoreForm(forms.Form):
    name = forms.CharField()    
    amt = forms.IntegerField() 
    recursive = forms.BooleanField(required=False)
    pay_type = forms.CharField()
    category = forms.ModelChoiceField(queryset=None)            
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(StoreForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=self.user)
