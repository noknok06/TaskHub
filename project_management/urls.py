# project_management/urls.py

from django.urls import path
from . import views
from .views import ProjectCreateView, JoinProjectView, TicketListView, TicketCreateView, TicketDetailView, ProjectListView, TicketUpdateView, AttachmentDeleteView
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, ProjectChartView, UserCreateView, ProjectAllChartView, UserProjectListView, LeaveProjectView, TicketsView, TicketDeleteView
from .views import upload_image

urlpatterns = [
    path('', views.home, name='home'),  # ホームページのURL (例として)
    path('register/', UserCreateView.as_view(), name='register_user'),
    path('create_project/', ProjectCreateView.as_view(), name='create_project'),
    path('join_project/', JoinProjectView.as_view(), name='join_project'), 
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),  # チケット詳細ページのURL
    path('ticket/<int:pk>/edit/', TicketUpdateView.as_view(), name='edit_ticket'),
    path('tickets/<int:pk>/delete/', TicketDeleteView.as_view(), name='delete_ticket'),
    path('tickets/', TicketsView.as_view(), name='tickets'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', TicketListView.as_view(), name='ticket_list'),
    path('projects/<int:project_id>/create_ticket/', TicketCreateView.as_view(), name='ticket_create'), 
    path('projects/<int:project_id>/categories/', CategoryListView.as_view(), name='category_list'),
    path('projects/<int:project_id>/categories/add/', CategoryCreateView.as_view(), name='category_create'),
    path('projects/<int:project_id>/categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('projects/<int:project_id>/categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('projects/<int:pk>/chart/', ProjectChartView.as_view(), name='project_chart'),
    path('projects/chart/', ProjectAllChartView.as_view(), name='project_all_chart'),
    path('update-task/', views.update_task, name='update_task'),
    path('my_projects/', UserProjectListView.as_view(), name='user_project_list'),
    path('join_project/', JoinProjectView.as_view(), name='join_project'),
    path('leave_project/<int:project_id>/', LeaveProjectView.as_view(), name='leave_project'),
    path('attachment/<int:pk>/delete/<int:ticket_id>/', AttachmentDeleteView.as_view(), name='delete_attachment'),
    path('upload_image/', upload_image, name='upload_image'),
    
]