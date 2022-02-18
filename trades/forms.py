from django import forms
from .models import TradeItem

class TradeItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['price'].required = True
        # self.fields['quantity'].required = True

    class Meta:
        model = TradeItem
        fields = []
        
class TradeOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['price'].required = True
        # self.fields['quantity'].required = True

    class Meta:
        model = TradeItem
        fields = []