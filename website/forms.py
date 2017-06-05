from django.contrib.auth.models import User
from django import forms
from website.models import Product, PaymentType, LineItem, UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

class UserProfileForm(forms.ModelForm):
    # address = forms.CharField(max_length=200, required=False)
    # phone = forms.CharField(max_length=200, required=False)

    class Meta:
        model = UserProfile
        fields = ('address', 'phone',)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'quantity', 'category', 'city', 'is_local')

class PaymentTypeForm(forms.ModelForm):

    class Meta:
        model = PaymentType
        fields = ('name', 'account_number',)

class AddToCartForm(forms.ModelForm):

    class Meta:
        model = LineItem
        fields = ('order', 'product',)
