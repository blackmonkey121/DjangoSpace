from django.views.generic import ListView, DetailView
# Create your views here.

from ..utils.mixin import NavViewMixin
from .models import Travel


class TravelView(NavViewMixin, ListView):

    model = Travel

    context_object_name = 'event_list'
    template_name = 'travel.html'

    paginate_by = 10


class TravelDetailView(NavViewMixin, DetailView):

    model = Travel

    context_object_name = 'event_list'
    template_name = 'travel.html'

    paginate_by = 10



