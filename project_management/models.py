from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.views.generic import CreateView
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name  # プロジェクト名を返す

class UserProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.project}"

class Ticket(models.Model):
    STATUS_CHOICES = [
        (10, '未処理'),
        (20, '保留'),
        (30, '確認中'),
        (40, '処理中'),
        (50, '完了'),
    ]
    title = models.CharField(max_length=255)
    detail = models.TextField(blank=True, null=True)
    status_id = models.IntegerField(choices=STATUS_CHOICES, default=10)
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 修正: CustomUser への外部キー
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Add this line
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時
    deadline = models.DateField(blank=True, null=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_tickets')
    companies = models.ManyToManyField('Company', blank=True, null=True)  # ManyToManyFieldとしてCompanyを設定


    def __str__(self):
        return self.title

    def __str__(self):
        return self.title
        
class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 修正: CustomUser への外部キー
    attachment_file = models.FileField(upload_to='comment_attachments/', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

class TicketFavorite(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 修正: CustomUser への外部キー

class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='attachments', on_delete=models.CASCADE)
    attachment_file = models.FileField(upload_to='attachments/')

    def __str__(self):
        return self.attachment_file.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        
class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name