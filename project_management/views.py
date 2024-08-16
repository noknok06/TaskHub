from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import ProjectForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project, UserProject, Ticket, TicketComment, TicketFavorite, Attachment, Category
from django.contrib.auth.decorators import login_required
from .forms import JoinProjectForm, TicketForm, CommentForm, CategoryForm, TicketSearchForm
from django.db.models import Count
import datetime


@login_required
def home(request):
    user_projects = UserProject.objects.filter(user=request.user)
    favorite_tickets = TicketFavorite.objects.filter(user=request.user).select_related('ticket')

    # ログインユーザーを取得
    user = request.user

    # ユーザーに割り当てられたチケットをステータスごとに集計
    ticket_status_counts = Ticket.objects.filter(assignee=user).values('status_id').annotate(count=Count('status_id'))

    # ステータスIDとそのカウントを辞書形式で準備
    status_counts = {
        10: 0,
        20: 0,
        30: 0,
        40: 0,
        50: 0
    }

    for item in ticket_status_counts:
        status_counts[item['status_id']] = item['count']

    # ユーザーが参加しているプロジェクトのIDを取得
    project_ids = user_projects.values_list('project_id', flat=True)
    
    # 更新があったチケットを取得（最新10件）
    updates = Ticket.objects.filter(
        project_id__in=project_ids
    ).order_by('-updated_at')[:10]  # `updated_at` フィールドが必要です

    # 期限が過ぎたチケットを取得
    overdue_tickets = Ticket.objects.filter(
        assignee=user,
        deadline__lt=datetime.date.today()
    )

    context = {
        'user_projects': user_projects,
        'favorite_tickets': favorite_tickets,
        'status_counts': status_counts,
        'updates': updates,  # 追加: 最新10件の更新履歴
        'overdue_tickets': overdue_tickets,  # 追加: 期限が過ぎたチケット
    }
    return render(request, 'home.html', context)

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(project_id=self.kwargs['project_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_id'])
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project_id'] = self.kwargs['project_id']
        return kwargs

    def get_success_url(self):
        return reverse_lazy('category_list', kwargs={'project_id': self.kwargs['project_id']})

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'

    def get_success_url(self):
        return redirect('category_list', project_id=self.kwargs['project_id'])

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    context_object_name = 'categories'

    def get_success_url(self):
        # Correctly pass project_id to the URL
        return reverse_lazy('category_list', kwargs={'project_id': self.kwargs['project_id']})

    def get_queryset(self):
        # Ensure that the queryset is filtered by project_id
        return Category.objects.filter(project_id=self.kwargs['project_id'])

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'create_project.html'
    fields = ['name', 'description', 'start_date', 'end_date']
    success_url = reverse_lazy('home')  # プロジェクト作成後にリダイレクトするURL

# def project_detail(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     return render(request, 'project_detail.html', {'project': project})

class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all()

class JoinProjectView(CreateView):
    model = UserProject
    form_class = JoinProjectForm
    template_name = 'join_project.html'
    success_url = reverse_lazy('home')  # 成功後にリダイレクトするURL

    def form_valid(self, form):
        # 現在ログインしているユーザーを取得
        form.instance.user = self.request.user
        return super().form_valid(form)

class TicketListView(ListView):
    model = Ticket
    template_name = 'ticket_list.html'
    context_object_name = 'tickets'
    form_class = TicketSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
        context['form'] = self.get_form()
        return context

    def get_form(self):
        return self.form_class(self.request.GET or None)

    def get_queryset(self):
        queryset = Ticket.objects.filter(project_id=self.kwargs['pk'])
        form = self.get_form()

        if form.is_valid():
            title = form.cleaned_data.get('title')
            status = form.cleaned_data.get('status')
            category = form.cleaned_data.get('category')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            deadline = form.cleaned_data.get('deadline')
            
            if title:
                queryset = queryset.filter(title__icontains=title)
            if status:
                queryset = queryset.filter(status_id=status)
            if category:
                queryset = queryset.filter(category__icontains=category)
            if start_date:
                queryset = queryset.filter(start_date__gte=start_date)
            if end_date:
                queryset = queryset.filter(end_date__lte=end_date)
            if deadline:
                queryset = queryset.filter(deadline__lte=deadline)

        return queryset

class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'create_ticket.html'

    def form_valid(self, form):
        # プロジェクトIDからProjectインスタンスを取得
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        form.instance.project = project  # Projectインスタンスを設定
        response = super().form_valid(form)
        # 添付ファイルの処理
        files = self.request.FILES.getlist('attachment_file')
        for file in files:
            Attachment.objects.create(ticket=self.object, attachment_file=file)
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # プロジェクトIDからProjectインスタンスを取得
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        kwargs['project'] = project  # Projectをフォームに渡す
        return kwargs

    def get_success_url(self):
        return reverse_lazy('ticket_list', kwargs={'pk': self.kwargs.get('project_id')})

class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['form'] = CommentForm()
        context['is_favorite'] = TicketFavorite.objects.filter(ticket=self.object, user=user).exists()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user

        if 'comment_form' in request.POST:
            # コメントの追加
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.ticket = self.object
                comment.user = user
                comment.save()
                return redirect('ticket_detail', pk=self.object.pk)
        
        elif 'is_favorite' in request.POST:
            # お気に入りの切り替え
            is_favorite = request.POST.get('is_favorite') == 'true'
            if is_favorite:
                TicketFavorite.objects.get_or_create(ticket=self.object, user=user)
            else:
                TicketFavorite.objects.filter(ticket=self.object, user=user).delete()
            
            return redirect('ticket_detail', pk=self.object.pk)
        
        return self.render_to_response(self.get_context_data())

# class TicketCommentCreateView(CreateView):
#     model = TicketComment
#     form_class = TicketCommentForm
#     template_name = 'ticket_detail.html'

#     def form_valid(self, form):
#         form.instance.ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])
#         form.instance.user = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy('ticket_detail', kwargs={'pk': self.kwargs['pk']})

class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'edit_ticket.html'

    def get_object(self, queryset=None):
        ticket = super().get_object(queryset)
        self.project = ticket.project  # チケットに関連するプロジェクトを取得して保持
        return ticket

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project  # プロジェクトをフォームに渡す
        return kwargs

    def get_success_url(self):
        # 編集後のリダイレクト先をチケット詳細ページに設定
        return reverse_lazy('ticket_detail', kwargs={'pk': self.object.pk})
