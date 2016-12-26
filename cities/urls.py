from django.conf.urls import url

from cities.views import delete_id_from_db
from . import views

urlpatterns = [
    url(r'^$', views.cities),
    url(r'^favorite$', views.favorite),
    url(r'^$', views.add_to_favorite, name='add_to_favorite'),
    url(r'^$', views.remove_from_favorite, name='remove_from_favorite'),
    url(r'^$', views.delete_id_from_db, name='delete_id_from_db'),

]
