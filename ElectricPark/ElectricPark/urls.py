"""
URL configuration for ElectricPark project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import get_addresses


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("landing_page/", views.landing_page, name="Landing Page"),
    path("login/choose_a_car/", views.choose_a_car, name="Choose A Car"),
    path("login/create_charging_sation/", views.create_charging_station, name="Create A Charging Station"),
    path("login/home/", views.home, name="home"),
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("login/active_orders/", views.active_orders, name="active orders"),
    path("login/order_history/", views.order_history, name="order history"),
    path("login/user_settings/", views.user_settings, name="user settings"),
    path("login/your_charging_stations/", views.charging_stations, name="your charging stations"),
    path("login/test_page/", views.test_page, name="test page"),
    path("login/uploade_csv/", views.upload_csv, name="upload_csv"),
    path("login/export_records/", views.export_records, name="export_records"),
    path("login/db_control/", views.DBcontrol, name="DBcontrol"),
    path('get_addresses/', get_addresses, name='get_addresses'),
    path('login/update_charging_station/', views.update_charging_station, name='update_charging_station'),
    #path('charging_stations/', views.charging_stations, name='charging_stations'),


]
