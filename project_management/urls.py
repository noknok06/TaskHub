# project_management/urls.py

from django.urls import path
from . import views
from .views import ProjectCreateView, JoinProjectView, TicketListView, TicketCreateView, TicketDetailView, ProjectListView, TicketUpdateView
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    path('', views.home, name='home'),  # ホームページのURL (例として)
    path('create_project/', ProjectCreateView.as_view(), name='create_project'),
    path('projects/<int:pk>/', TicketListView.as_view(), name='ticket_list'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('join_project/', JoinProjectView.as_view(), name='join_project'), 
    path('project/<int:project_id>/create_ticket/', TicketCreateView.as_view(), name='ticket_create'), 
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),  # チケット詳細ページのURL
    path('ticket/<int:pk>/edit/', TicketUpdateView.as_view(), name='edit_ticket'),
    path('projects/<int:project_id>/categories/', CategoryListView.as_view(), name='category_list'),
    path('projects/<int:project_id>/categories/add/', CategoryCreateView.as_view(), name='category_create'),
    path('projects/<int:project_id>/categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('projects/<int:project_id>/categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]