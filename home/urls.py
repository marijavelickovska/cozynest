from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about_us', views.about_us, name='about_us'),
    path('careers', views.careers, name='careers'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('our_team', views.our_team, name='our_team'),
    path("newsletter/", views.newsletter_signup, name="newsletter_signup"),
]
