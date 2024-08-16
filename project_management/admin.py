from django.contrib import admin
from .models import CustomUser, Project, UserProject, Ticket, Attachment, Category, TicketComment, TicketFavorite

admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(UserProject)
admin.site.register(Ticket)
admin.site.register(Attachment)
admin.site.register(Category)
admin.site.register(TicketComment)
admin.site.register(TicketFavorite)
