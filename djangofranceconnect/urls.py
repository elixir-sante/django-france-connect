# Import Django stuff
from django.contrib import admin
from django.urls import path, include

#import djangofranceconnect.franceconnect as franceconnect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djangofranceconnect.franceconnect.urls')),
]
