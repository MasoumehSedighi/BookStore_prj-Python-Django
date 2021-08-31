from django import forms


class CouponForm(forms.Form):
	code = forms.CharField()


class AddressOrderForm(forms.Form):
	city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
