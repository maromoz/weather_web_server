"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from cities import views

urlpatterns = [
    url(r'^$', views.get_favorite),
    url(r'^get_cities/', views.get_cities),
    url(r'^get_city_temp/', views.get_city_temp),
    url(r'^admin/', admin.site.urls),
    url(r'^get_favorite/', views.get_favorite),
    url(r'^add_city_to_favorite/', views.add_city_to_favorite),
    url(r'^remove_city_from_favorite/', views.remove_city_from_favorite),
    url(r'^delete_id_from_db/', views.delete_id_from_db),
    url(r'^add_id_to_db/', views.add_id_to_db),
    url(r'^get_auto_complete_cities/', views.get_auto_complete_cities),

]

