#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from dal import autocomplete
from django import forms
from mdeditor.fields import MDTextFormField
from xadmin.layout import Fieldset, Row

from .models import Travel, Province


class TravelAdminForm(forms.ModelForm):

    context = MDTextFormField(label='旅途描述', required=False, )

    province = forms.ModelChoiceField(
        queryset=Province.objects.values('id', 'name').filter(status=Province.STATUS_NORMAL),
        widget=autocomplete.ModelSelect2(url='province-autocomplete'),
        label='省份',
    )

    class Meta:
        model = Travel
        fields = (
            'title', 'context', 'visit',
            'status', 'province'
        )