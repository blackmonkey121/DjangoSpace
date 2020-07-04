"""MySpace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin

from .rss import LastesPostFeed

from .autocomplete import TagAutoComplete, CategoryAutoComplete, ProvinceComplete
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path, include, re_path
from django.views.static import serve

from MySpace import settings
from apps.home.views import HomeView
from .sitemap import ArticleSitemap


urlpatterns = [
    path('admin/', xadmin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    path('home/', include(('apps.home.urls', 'home'), namespace='home')),
    path('picture/', include(('apps.picture.urls', 'picture'), namespace='picture')),
    path('life/', include(('apps.life.urls', 'life'), namespace='life')),
    path('article/', include(('apps.article.urls', 'article'), namespace='article')),
    path('travel/', include(('apps.travel.urls', 'travel'), namespace='travel')),
    path('mdeditor/', include(('mdeditor.urls', 'mdeditor'), namespace='mdeditor')),

    path('category-autocomplete/', CategoryAutoComplete.as_view(), name='category-autocomplete'),
    path('tag-autocomplete/', TagAutoComplete.as_view(), name='tag-autocomplete'),

    path('province-autocomplete/', ProvinceComplete.as_view(), name='province-autocomplete'),

    path('', HomeView.as_view(), name='home'),
    path('rss', LastesPostFeed(), name='rss'),
    path('sitemap.xml', sitemap_views.sitemap, {'sitemaps': {'articles': ArticleSitemap}}),

]
