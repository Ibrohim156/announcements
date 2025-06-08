from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reg/', views.register_view, name='reg'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_property, name='add_property'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('delete-property/<int:property_id>/', views.delete_property, name='delete_property'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/<int:property_id>/leave-request/', views.leave_request, name='leave_request'),
    path('my-requests/', views.my_requests, name='my_requests'),
     path('', views.property_list, name='property_list'),
     path('about/', views.about, name='about'),


]





