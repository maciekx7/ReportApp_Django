from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.core.files.storage import FileSystemStorage
from aplikacja_raportowanie.validators import validate_file_size
from django.core.validators import FileExtensionValidator
import requests
# Create your models here.



STATUS_CHOICES = (
        ("nowy", "nowy"),
        ("do podjęcia", "do podjęcia"),
        ("w obserwacji", "w obserwacji"),
        ("wstrzymane", "wstrzymane"),
        ("przekazane", "przekazane"),
        ("w realizacji", "w realizacji"),
        ("zamknięte", "zamknięte"),
    )

list_of_extensions = ['pdf', 'jpg','jpeg', 'png','gif','bmp', 'txt', 'doc', 'docx','dot','docm','dotm','xml','odt','dotx', 'xls', 'xlsx', 'xlsb', 'xslm', 'xltx', 'xlt', 'ods', 'ppt', 'pptx', 'potx', 'pot', 'odp', 'pps', 'ppsx','pptm', 'potm','ppsm']

class Post(models.Model):
    publisher = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='publisher_article_set')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='author_article_set', blank=True, null=True)
    title = models.CharField(max_length=150)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default = 'nowy')
    text = models.TextField()
    start_date = models.DateTimeField()
    publish_date = models.DateTimeField()
    modify_date = models.DateTimeField(blank=True, null=True)
    QM_id = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True)
    tictet_number = models.CharField(max_length = 30, blank = True, null = True)
    is_deleted = models.BooleanField(default = False)
    long_term = models.BooleanField(default = False)
    change = models.TextField(max_length = 20, blank=True, null=True)
    file = models.FileField(
        upload_to = "", null=True, blank=True,
        validators=[validate_file_size, FileExtensionValidator(list_of_extensions)])
    history = HistoricalRecords()



    def publish(self, request, start_date, start_time, status):
        self.publish_date = timezone.now()
        self.publisher = request.user
        if status != "do podjęcia":
            self.author = request.user
        self.change = "Stworzyłem"
        self.start_date = start_date + ' ' + start_time
        self.save_file()
        self.save()

    def edit(self, start_date, change, status):
        self.start_date = start_date
        self.modify_date = timezone.now()
        self.change = change
        if status == "do podjęcia":
            self.author = None
        self.save_file()
        self.save()

    def author_change(self, new_post_author, change):
        self.modify_date = timezone.now()
        self.author =  User.objects.get(username=new_post_author)
        self.change = change
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_file_url(self):
        if self.file.name:
            file_f = FileSystemStorage()
            return file_f.url(self.file.name)
        else:
            return ""

    def save_file(self):
        if self.file.name:
            file_f = FileSystemStorage()
            file_f.save(self.file.name, self.file)

    def if_there_is_a_file_return_text(self):
        file_f = FileSystemStorage()
        if file_f.url(self.file.name) == "/media/":
            return ""
        else:
            return "załącznik"

    def if_post_have_file_icon(self):
        if self.file.name:
            return "fas fa-file"

    def get_ticket_number_icon(self):
        if self.tictet_number:
            return "fas fa-book-open"

    def get_ticket_number(self):
        if self.tictet_number:
            return self.tictet_number
        else:
            return ""

    def get_author(self):
        if self.author:
            return self.author
        else:
            return ""

    def get_Qm_id(self):
        if self.QM_id:
            return self.QM_id
        else:
            return ""

    def get_QM_id_icon(self):
        if self.QM_id:
            return "fas fa-lightbulb"
        else:
             return ""



class Comment(models.Model):
    text = models.TextField()
    publish_date = models.DateTimeField(default = timezone.now)
    post_id = models.ManyToManyField(Post)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default = False)
    file = models.FileField(upload_to = "comments/", null=True, blank=True, validators=[validate_file_size, FileExtensionValidator(['pdf', 'jpg', 'png', 'txt'])])
    history = HistoricalRecords()

    def publish(self, request):
        self.publish_date = timezone.now()
        self.author = request.user
        self.save_file()
        self.save()

    def edit(self):
        self.save_file()
        self.save()

    def __str__(self):
        return self.text

    def get_absolute_file_url(self):
        if self.file.name:
            file_f = FileSystemStorage()
            return file_f.url(self.file.name)
        else:
            return ""

    def save_file(self):
        if self.file.name:
            file_c = FileSystemStorage()
            file_c.save(self.file.name, self.file)

    def if_there_is_a_file_return_text(self):
        if self.file.name:
            return "ZAŁĄCZNIK"
        else:
            return ""


    def if_comment_have_file_icon(self):
        if self.file.name:
            return "fas fa-file"
