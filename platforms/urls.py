from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='platforms_index'),                         # GET/POST /platforms/
    path('<int:id>/', views.show, name='platforms_show'),                  # GET/PUT/PATCH/DELETE /platforms/5/
]
