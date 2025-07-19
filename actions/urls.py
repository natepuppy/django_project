from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='actions_index'),                         # GET/POST /actions/
    path('<int:id>/', views.show, name='actions_show'),                  # GET/PUT/PATCH/DELETE /actions/5/
]
