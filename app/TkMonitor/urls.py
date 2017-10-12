from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ltmon/$'                     , views.LTMonView.as_view() , name='ltmon'),
    url(r'^ltmon/getObj/$'              , views.GetJSONForLTMon     , name='ltmon_getObj'),
    url(r'^rtmon/$'                     , views.RTMonView.as_view() , name='rtmon'),
]
