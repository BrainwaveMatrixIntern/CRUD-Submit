from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from Inv.models import Category, Item  

class RegForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ItemAddForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    class Meta:
        model = Item
        fields = ["name", "quantity", "category"]