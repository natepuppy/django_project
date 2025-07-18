from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='platform_users_index'),                         # GET/POST /platform_users/
    path('<int:id>/', views.show, name='platform_users_show'),                  # GET/PUT/PATCH/DELETE /platform_users/5/
]
