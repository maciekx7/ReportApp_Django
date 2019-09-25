from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Post, Comment
import requests
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from datetime import date
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.defaults import page_not_found
from django.db.models import Q, F
