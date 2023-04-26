from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('search-task', views.search_task, name='search-task'),
    path('add_card', views.add_card, name='add_card'),
    path('<int:pk>', views.view, name='views_detail'),
    path('<int:pk>/update', views.edit, name='update'),
    path('<int:pk>/delete', views.PictureDelete.as_view(), name='delete'),
    path('<int:pk>/add_movement', views.add_movement, name='add_movement'),
]