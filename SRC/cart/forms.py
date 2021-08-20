from django import forms


class CartAddForm(forms.Form):
    """این فرم شامل تعداد محصول انتخابی برای سبد میباشد که بین 1 تا 9 عدد ار آن کتاب را میتوانیم انتخاب کنبم"""
    quantity = forms.IntegerField(min_value=1, max_value=9)


