"""IgCrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url


from app01 import views



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^get_valid_img/', views.get_valid_img),
    url(r'^reg/', views.reg),
    url(r'^logout/', views.logout),
    url(r'^index/', views.index),
    url(r'^$', views.index),
    url(r'^customers/list/', views.CustomerView.as_view(),name="customers_list"),
    url(r'^mycustomers/', views.CustomerView.as_view(),name="mycustomers"),
    url(r'^customer/add/', views.AddEditCustomerView.as_view(),name="addcustomers"),
    url(r'^customer/edit/(\d+)', views.AddEditCustomerView.as_view(),name="editcustomers"),
    url(r'^consult_records/', views.ConsultRecordView.as_view(),name="consult_records"),
    url(r'^consult_records/add/', views.AddEditConsultRecordView.as_view(), name="add_consult_records"),
    url(r'^consult_records/edit/(\d+)', views.AddEditConsultRecordView.as_view(), name="edit_consult_records"),
]
