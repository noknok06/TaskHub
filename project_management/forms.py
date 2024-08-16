# project_management/forms.py

from django import forms
from .models import Project, UserProject, Ticket, TicketComment, CustomUser, Attachment, Category

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']

class JoinProjectForm(forms.ModelForm):
    class Meta:
        model = UserProject
        fields = ['project']  # プロジェクトのみを選択できるようにする

class CommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['comment', 'attachment_file']  

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'detail', 'status_id', 'assignee', 'category', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['category'].queryset = Category.objects.filter(project=project)

class TicketAttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['attachment_file']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'project']
        widgets = {
            'project': forms.HiddenInput()  # プロジェクトIDを隠しフィールドとして送信
        }

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        if project_id:
            self.fields['project'].initial = project_id