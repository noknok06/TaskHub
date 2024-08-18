from django.contrib import admin
from .models import CustomUser, Project, UserProject, Ticket, TicketComment, TicketFavorite, Attachment, Category

# Custom admin for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name')

# Custom admin for Project
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date')
    search_fields = ('name', 'description')

# Custom admin for UserProject
class UserProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')
    search_fields = ('user__email', 'project__name')

# Custom admin for Ticket
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status_id', 'assignee', 'category', 'start_date', 'end_date', 'project', 'updated_at', 'deadline')
    list_filter = ('status_id', 'assignee', 'category', 'project')
    search_fields = ('title', 'assignee__email', 'category__name', 'project__name')
    # Optional: Add a read-only field or fields
    readonly_fields = ('updated_at',)

    # Custom method to display detailed view of Ticket
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # You can annotate or modify queryset as needed here
        return queryset

# Custom admin for TicketComment
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'comment', 'create_date', 'attachment_file')
    search_fields = ('ticket__title', 'user__email', 'comment')
    list_filter = ('ticket', 'user')

# Custom admin for TicketFavorite
class TicketFavoriteAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user')
    search_fields = ('ticket__title', 'user__email')

# Custom admin for Attachment
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'attachment_file')
    search_fields = ('ticket__title', 'attachment_file')

# Custom admin for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project')
    search_fields = ('name', 'project__name')

# Register the admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(UserProject, UserProjectAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketComment, TicketCommentAdmin)
admin.site.register(TicketFavorite, TicketFavoriteAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Category, CategoryAdmin)
