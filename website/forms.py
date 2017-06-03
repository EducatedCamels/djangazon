from django.contrib.auth.models import User 
from django import forms
from website.models import Product, PaymentType, LineItem

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'quantity', 'city', 'is_local', 'photo',)  

class PaymentTypeForm(forms.ModelForm):

    class Meta:
        model = PaymentType
        fields = ('name', 'account_number',)

class AddToCartForm(forms.ModelForm):

    class Meta:
        model = LineItem
        fields = ('order', 'product',)
