from django.views.generic import View

# Create your views here.
from ..utils.mixin import rich_render


class HomeView(View):

    def get(self, request, *args, **kwargs):
        return rich_render(request, 'home.html')


class AboutMe(View):

    def get(self, request, *args, **kwargs):
        return rich_render(request, 'me.html')
