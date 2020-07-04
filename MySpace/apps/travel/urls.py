#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import xadmin
from django.urls import path
from .views import TravelView

urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('', TravelView.as_view(), name='travel'),
    path('province/<int:id>', TravelView.as_view(), name='province'),
    path('province/<int:p_id>/city/<int:c_id>', TravelView.as_view(), name='city'),
]