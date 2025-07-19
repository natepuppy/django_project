from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='logs_index'),                         # GET/POST /logs/
    path('<int:id>/', views.show, name='logs_show'),                  # GET/PUT/PATCH/DELETE /logs/5/
]
