from django.conf.urls import url
from . import views

urlpatterns = [
    url('home',views.index,name='index'),
    url('export-csv',views.exportCSV,name='export-csv'),
]