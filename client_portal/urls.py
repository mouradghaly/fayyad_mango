from . import views
from django.urls import path 
urlpatterns = [
    path("", views.order, name='order' ),
    path("admin", views.admin, name='admin' ),
    path("dashboard", views.dashboard, name="dashboard"), 
    path("dashboard1", views.dashboard_complete, name="completed"),
    path("updatestatus", views.update_status, name="update"), 
    path("prices", views.price, name="price"  ), 
    path("track_order", views.track_order, name="track")
]