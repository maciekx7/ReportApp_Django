from django import forms
import datetime
from .models import Post, Comment, STATUS_CHOICES

class PostForm(forms.ModelForm):
    title = forms.CharField(label="Tytuł*")
    text = forms.CharField(label="Treść*", widget=forms.Textarea)
    QM_id = forms.DecimalField(max_digits=20, decimal_places=0, required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Status*")
    file = forms.FileField(label="Załącznik", help_text='max. 20MB', required=False)
    tictet_number = forms.CharField(label="TW/SWING ticket", required=False)
    long_term = forms.BooleanField(label = "Problem dugotrwaly", required=False)
    class Meta:
        model = Post
        fields = ('title',"text","long_term", "status", "QM_id", "tictet_number", "file")

class CommentForm(forms.ModelForm):
    text = forms.CharField(label = "Treść*", widget=forms.Textarea)
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Status*")
    file = forms.FileField(label = "Załącznik", help_text='max. 20MB', required=False)
    class Meta:
        model = Comment
        fields = ('text', 'status', 'file')
