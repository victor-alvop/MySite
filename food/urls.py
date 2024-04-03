from . import views
from django.urls import path

app_name = 'food'

urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.items, name='items'),
    path('<int:item_id>/', views.detail, name='detail')
]