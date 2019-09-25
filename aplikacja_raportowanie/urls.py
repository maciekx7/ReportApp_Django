from django.urls import path
#from . import views
from aplikacja_raportowanie import views
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


app_name = 'raportowanie'

urlpatterns = [
	path('', views.users_index, name="users_index"),
	path('list/', views.index, name = 'index'),
	path('list/quater/', views.index_quater, name='quater'),
	path('list/closed', views.index_closed, name='index_closed'),
	path('closed/', views.users_index_closed, name='users_index_closed'),
	path('long_terms/', views.long_index, name="long_terms"),
	path('list/usuniete/', views.index_deleted, name = "deleted_posts_index"),
	path('post/new/', views.post_new, name = 'post_new'),
	path('post/<int:post_id>/',  views.post_filled, name="post_filled"),
	path('post/<int:post_id>/edit/', views.post_edit, name="post_edit"),
	path('post/<int:post_id>/history', views.post_history, name="post_history"),
	path('post/<int:post_id>/deleted', views.delete_post, name="post_delete"),
	path('post/<int:post_id>/comment_delete/<int:comment_id>', views.delete_comment, name="comment_delete"),
	path('author_changing/<int:post_id>/', views.author_post_change, name = "author_post_change"),
	path('post/<int:post_id>/comment_history/<int:comment_id>/', views.comment_history, name = "comment_history"),
	path('post/<int:post_id>/comment_edit/<int:comment_id>', views.comment_edit, name="comment_edit"),
	path('login/', views.login_view, name="login"),
	path('logout/', views.logout_view, name="logout_"),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'aplikacja_raportowanie.views.handler404'
