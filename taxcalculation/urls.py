from django.urls import include, path

from taxcalculation import views

app_name = 'taxcalculation'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('file/<int:id>/',views.file_detail, name='file_detail')
]