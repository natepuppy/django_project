from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sessions_index'),                         # GET/POST /sessions/
    path('<int:id>/', views.show, name='sessions_show'),                  # GET/PUT/PATCH/DELETE /sessions/5/
]
