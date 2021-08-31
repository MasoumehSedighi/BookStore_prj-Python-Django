from django import forms
from django.forms import TextInput, BooleanField

from accounts.models import Addresses


class CouponForm(forms.Form):
	code = forms.CharField()


class AddressOrderForm(forms.Form):
	city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
