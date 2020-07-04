#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


from django import forms
from .models import Album, Image


class AlbumAdminForm(forms.ModelForm):

    desc = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 100px; width:100%; resize:none;'}), label='描述', required=False)

    class Meta:
        model = Album
        fields = (
            'desc', 'name',
            'cover', 'status', 'visit',
        )


class ImageAdminForm(forms.ModelForm):

    desc = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 60px; width:100%; resize:none;'}), label='描述', required=False)

    class Meta:
        model = Image
        fields = (
            'desc', 'status', 'visit', 'album','img'
        )