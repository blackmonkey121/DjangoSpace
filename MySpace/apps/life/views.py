from ..utils.mixin import rich_render as render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Cooking, Book, Note, Perception
from ..utils.mixin import NavViewMixin


class MixinViewDetail(object):
    """ """


class LifeView(NavViewMixin, View):

    def get(self, request, *args, **kwargs):

        return render(request, 'life.html')


class CookingView(NavViewMixin, MixinViewDetail, ListView):
    """ TODO: """

    model = Cooking

    context_object_name = 'cooking_list'

    paginate_by = 10

    def get(self, request, *args, **kwargs):

        return render(request, 'life.html')


class BookView(NavViewMixin, MixinViewDetail, ListView):
    model = Book

    context_object_name = 'book_list'

    paginate_by = 10

    def get(self, request, *args, **kwargs):

        return render(request, 'life.html')


class NoteView(NavViewMixin, MixinViewDetail, ListView):
    model = Note

    context_object_name = 'note_list'

    paginate_by = 10

    def get(self, request, *args, **kwargs):

        return render(request, 'life.html')


class PerceptionView(NavViewMixin, MixinViewDetail, ListView):
    model = Perception

    context_object_name = 'perception_list'

    paginate_by = 10

    def get(self, request, *args, **kwargs):

        return render(request, 'life.html')


class CookingDetailView(NavViewMixin, MixinViewDetail, DetailView):
    """ TODO: """

    model = Cooking

    context_object_name = 'cooking_list'

    paginate_by = 10

    def get(self, request, *args, **kwargs):

        return render(request, 'life.html')


class BookDetailView(NavViewMixin, MixinViewDetail, DetailView):
    model = Book

    context_object_name = 'book_list'

    paginate_by = 10

    def get(self, request, *args, **kwargs):

        return render(request, 'life.html')


class NoteDetailView(NavViewMixin, MixinViewDetail, DetailView):
    model = Note

    context_object_name = 'note_list'

    paginate_by = 10

    def get(self, request, *args, **kwargs):

        return render(request, 'life.html')


class PerceptionDetailView(NavViewMixin, MixinViewDetail, DetailView):
    model = Perception

    context_object_name = 'perception_list'

    paginate_by = 10

    def get(self, request, *args, **kwargs):

        return render(request, 'life.html')
