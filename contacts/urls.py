from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='contacts_index'),                         # GET/POST /contacts/
    path('<int:id>/', views.show, name='contacts_show'),                  # GET/PUT/PATCH/DELETE /contacts/5/
]
