# Import Django stuff
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('connect/', views.connect, name="fc_connect"),
    path('disconnect/', views.disconnect, name = "fc_disconnect"),
    path('callback/', views.callback_login, name="fc_callback_login"),
    path('logout/', views.callback_logout, name="fc_callback_logout"),
]
