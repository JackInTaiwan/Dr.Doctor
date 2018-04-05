"""biofinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# Import view functions from chatroom app.
import doctor.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^reg/$', doctor.views.reg),
    #url(r'^accounts/','registration.backends.simple.urls'),
    url(r'^cover/$', doctor.views.cover),
    url(r'^chatroom/$', doctor.views.chatroom),
    #url(r'^welcome/$', welcome)

]



