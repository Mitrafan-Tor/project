from django.urls import path    # типо board
from .views import IndexView     # типо board


# типо board
urlpatterns =[
    path('', IndexView.as_view()),
]