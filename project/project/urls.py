from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('simpleapp/', include('simpleapp.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
   path('appointments/', include(('appointments.urls'), namespace='appointments')),
   path('', include('protect.urls')),
]