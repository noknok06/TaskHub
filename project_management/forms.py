# project_management/forms.py

from django import forms
from .models import Project, UserProject, Ticket, TicketComment, CustomUser, Attachment, Category


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password']
        
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
        fields = ['title', 'detail', 'status_id', 'assignee', 'category', 'start_date', 'end_date', 'deadline', 'parent']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['category'].queryset = Category.objects.filter(project=project)
        if self.instance:
            self.fields['start_date'].initial = self.instance.start_date
            self.fields['end_date'].initial = self.instance.end_date
            self.fields['deadline'].initial = self.instance.deadline

        # 親チケットを選択するためのフィールドを追加
        self.fields['parent'].queryset = Ticket.objects.filter(project=project).exclude(id=self.instance.id)
        
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

class TicketSearchForm(forms.Form):
    title = forms.CharField(required=False, label='Title')
    status = forms.ChoiceField(choices=[('', 'Any')] + list(Ticket.STATUS_CHOICES), required=False, label='Status')
    category = forms.CharField(required=False, label='Category')
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label='Start Date')
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label='End Date')
    deadline = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label='Deadline')
