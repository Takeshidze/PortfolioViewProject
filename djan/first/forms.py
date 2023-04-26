import datetime
import os
from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, \
    NumberInput, Select, DateTimeField, MultiWidget
from django.utils.timezone import make_aware

from .models import Galery, Category, Objects, Movement


class MinimalSplitDateTimeMultiWidget(MultiWidget):

    def __init__(self, widgets=None, attrs=None):
        if widgets is None:
            if attrs is None:
                attrs = {}
            date_attrs = attrs.copy()

            date_attrs['type'] = 'date'

            widgets = [
                TextInput(attrs=date_attrs),
            ]
        super().__init__(widgets, attrs)

    # nabbing from https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#django.forms.MultiWidget.decompress
    def decompress(self, value):
        if value:
            return [value.date(), value.strftime('%H:%M')]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        date_str = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.

        if date_str == '':
            return None

        my_datetime = datetime.datetime.strptime(*date_str, "%Y-%m-%d")
        # making timezone aware
        return make_aware(my_datetime)


class AddMovement(ModelForm):
    departure_date = DateTimeField(widget=MinimalSplitDateTimeMultiWidget(attrs={'class': 'uk-input'}))
    arrival_date = DateTimeField(widget=MinimalSplitDateTimeMultiWidget(attrs={'class': 'uk-input'}))

    class Meta:
        model = Movement
        fields = {'departure_date', 'arrival_date', 'first_location', 'second_location'}
        widgets = {
            "first_location": Select(attrs={
                'class': 'uk-select uk-form-width-medium',
            }, ),
            "second_location": Select(attrs={
                'class': 'uk-select uk-form-width-medium',
            }, )
        }


class AddCategory(ModelForm):
    class Meta:
        model = Category
        fields = {'category'}
        widgets = {
            "category": TextInput(attrs={
                'class': 'uk-input uk-margin uk-form-width-auto',
                'placeholder': 'Новая категория'})
        }


class AddObject(ModelForm):
    class Meta:
        model = Objects

        fields = {'object'}
        widgets = {
            "object": TextInput(attrs={
                'class': 'uk-input uk-margin uk-form-width-auto',
                'placeholder': 'Новый объект'})
        }


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            "username": TextInput(attrs={
                'class': 'uk-input',
                'placeholder': 'Название'
            }),
            "password": TextInput(attrs={
                'class': 'uk-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class GallaryAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"
        self.fields['obj'].empty_label = "Объект не выбран"
        self.fields['dir'].required = False

    # date = forms.DateField(widget=widgets.AdminDateWidget(attrs={'class': 'uk-input', 'type': 'date'}))
    date = DateTimeField(widget=MinimalSplitDateTimeMultiWidget(attrs={'class': 'uk-input'}))

    class Meta:
        model = Galery
        fields = ['name', 'author', 'sizeX', 'sizeY', 'obj', 'img',
                  'description', 'category', 'date', 'dir', 'material']

        widgets = {
            "name": TextInput(attrs={
                'class': 'uk-input',
                'placeholder': 'Название'
            }),
            "author": TextInput(attrs={
                'class': 'uk-input',
                'placeholder': 'Автор'
            }),
            "sizeX": NumberInput(attrs={
                'class': 'uk-input',
                'placeholder': 'Размер по X'
            }),
            "sizeY": NumberInput(attrs={
                'class': 'uk-input',
                'placeholder': 'Размер по Y'
            }),
            "description": Textarea(attrs={
                'class': 'uk-textarea',
                'placeholder': 'Описание'
            }),
            "material": TextInput(attrs={
                'class': 'uk-input',
                'placeholder': 'Материал',
            }),
            "dir": TextInput(attrs={
                'class': 'uk-input',
                'placeholder': 'Папка',
            }),
            "obj": Select(attrs={
                'class': 'uk-select uk-form-width-medium',
            }, ),
            "category": Select(attrs={
                'class': 'uk-select uk-form-width-medium',
            })
        }
