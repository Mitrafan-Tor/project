from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('simpleapp/', include('simpleapp.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
   path('appointment/', include(('appointment.urls'), namespace='appointment')),
   path('', include('protect.urls')),
   path('board/', include('board.urls')),
]