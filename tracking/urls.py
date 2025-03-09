from django.urls import path
from .views import  track_view

urlpatterns = [
    # path("", index, name="index"),  # Default page
    path("track/", track_view, name="track"),  # Track page
]
# from django.urls import path
# from .views import track_view  # Import the function from views.py

# urlpatterns = [
#     path("", index, name="index"),  # Default page
#     path("track/", track_view, name="track"),  # Track page
    
# ]