from django import forms
from .models import Order, Address

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 51)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='تعداد')


class OrderForm(forms.Form):
    address = forms.ModelChoiceField(queryset=Address.objects.none(), label='آدرس')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['address'].queryset = Address.objects.filter(user_id=user.id)
