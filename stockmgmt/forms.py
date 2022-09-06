from dataclasses import field, fields
from django import forms
from .models import Stock

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quality']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category :
            raise forms.ValidationError('This field is required')

        #for instance in Stock.objects.all():
            if instance.category == category:
                raise forms.ValidationError(category + 'is already taken')
        return category
        
    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name

class StockSearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['category', 'item_name']

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quality']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields =['issue_quantity', 'issue_to']

class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields =['receive_quantity', 'issue_by']

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']
