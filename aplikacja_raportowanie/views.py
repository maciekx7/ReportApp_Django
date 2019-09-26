from aplikacja_raportowanie.functions_to_view import *
from aplikacja_raportowanie.view_class import *


#Funkcja wypełniająca stronę początkową uzytkownika
@login_required(login_url="/login/")
def users_index(request):
	users_index = View_type(request, which_index_view(request, "user_index"), which_index_view(request, "posts_to_do"), f"Twoje aktywne zgłoszenia ({logged_user(request)})")
	return users_index.render_view(request)

#Funkcja wypełniająca stronę początkową grupy
@login_required(login_url="/login/")
def index(request):
	index = View_type(request, which_index_view(request, "index"), which_index_view(request, "posts_to_do"), "Aktywne zgłoszenia grupy")
	return index.render_view(request)

#Wyświetl tylko zamknięte zgłoszenia użytkownika
@login_required(login_url="/login/")
def users_index_closed(request):
	index = View_type(request, which_index_view(request, "users_index_closed"),False, f"Twoje zamknięte zgłoszenia ({logged_user(request)})")
	return index.render_view(request)

#Wyświetl tylko zamknięte zgłoszenia grupy
@login_required(login_url="/login/")
def index_closed(request):
	index = View_type(request, which_index_view(request, "index_closed"),False, "Wszystkie zamknięte zgłoszenia")
	return index.render_view(request)

#Wyświetla listę usuniętych zgłoszeń
@login_required(login_url="/login/")
def index_deleted(request):
	index = View_type(request, which_index_view(request, "index_deleted"),False, "Wszystkie usunięte zgłoszenia")
	return index.render_view(request)

@login_required(login_url="/login/")
def long_index(request):
	index = View_type(request, which_index_view(request, "long_index"), False, "Zgłoszenia dlugoterminowe")
	return index.render_view(request)

#Wyświetla widok postów filtrowanych po kwartale
@login_required(login_url="/login/")
def index_quater(request):
	if request.method == "POST":
		start_date = request.POST['pic-a-date-start-']
		stop_date = request.POST['pic-a-date-stop-']
		date = str(start_date) + " 00:00", str(stop_date) + " 23:59"
		status = request.POST.getlist('status-pick-a-quater')
		author = str(request.POST['author-pick-a-quater'])
		what_ = str(request.POST['what-state-pick-a-quater'])
		date_type = str(request.POST['date'])
		print(date_type)
		posts = which_quater(request, date, status, author, what_, date_type)
		view_type = str(quater_string(date)) + ", " + str(status_name_filter(str(status))) + ", " + author + ", " + what_.replace('-', "/", 1).replace('_', ' ')
		index = View_type(request, posts,False, view_type)
		return index.render_view(request)
	else:
		return redirect('raportowanie:index')

#Wyświetla historię edycji posta
@login_required(login_url="/login/")
def post_history(request, post_id):
	try:
		post_history = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		return handler404(request,None)
	content = {
		"post_history": post_history.history.all(),
		"post": post_history
	}
	return render(request, 'aplikacja_raportowanie/post_history.html', content)


#Wyświetla historię edycji komentarza
@login_required(login_url="/login/")
def comment_history(request, post_id, comment_id):
	try:
		comment_history = Comment.objects.get(id=comment_id)
	except Comment.DoesNotExist:
		return handler404(request,None)

	content = {
		"comment_history": comment_history.history.all(),
		"post": Post.objects.get(id=post_id)
	}
	return render(request, 'aplikacja_raportowanie/comment_history.html', content)



#Usuwa posta z głównej listy i przenosi go na listę usunięte
@login_required(login_url="/login/")
def delete_post(request,post_id):
	try:
		post = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		return handler404(request,None)
	if post.is_deleted == True:
		pass
	else:
		post.is_deleted = True
		post.modify_date = timezone.now()
		post.status = "zamknięte"
		post.change = "Usunięcie"
		post.save()
		comment = Comment(text="USUWAM", publish_date = timezone.now(), status="USUWANIE zgłoszenia", author=logged_user(request))
		comment.save()
		comment.post_id.add(post.id)
	return redirect('raportowanie:post_filled', post_id=post.id)

@login_required(login_url="/login/")
def delete_comment(request, post_id, comment_id):
	try:
		post = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		return handler404(request,None)
	if request.method == "POST":
		try:
			comment = Comment.objects.get(id=comment_id)
		except Comment.DoesNotExist:
			return handler404(request,None)

		if comment.is_deleted == True:
			pass
		else:
			comment.is_deleted = True
			comment.modify_author = logged_user(request)
			comment.save()
			post.change = f"Usunięto koemntarz {comment_id}"
			post.save()
	return redirect('raportowanie:post_filled', post_id=post.id)


#Funkcja wypelniająca stronę z istniejcym zgłoszeniem i daje możliwość komentowania
@login_required(login_url="/login/")
def post_filled(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		return handler404(request,None)
	if request.method == "POST":
		form = CommentForm(request.POST, request.FILES)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.publish(request)
			post_first_status = post.status
			post.status = comment.status
			if post.status == "do podjęcia":
				post.author = None
			else:
				post.author = request.user
			post.change = status_change_field(post_first_status, post.status, "Zamknięcie", "Ponowne otwarcie", "Dodanie komentarza", "Ponowne otwarcie, do podjęcia", "Podjęcie zgłoszenia")
			post.modify_date = timezone.now()
			post.save()
			comment.post_id.add(str(post.id))
	else:
		form = CommentForm()

	comments = Comment.objects.filter(is_deleted = False, post_id=post.id).order_by("-publish_date")

	content = {
		"login_user": logged_user(request),
		"post" : post,
		"comments": comments,
		"status_color": status_colors(post),
		"form": form,
		"users": list_of_users(),
		 }
	return render(request, 'aplikacja_raportowanie/post_filled.html', content)

#Funkcja do wyswietlania strony pozwalającej tworzyć nowe zgłoszenie
@login_required(login_url="/login/")
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			start_date = request.POST['post-start-date']
			start_time = request.POST['post-start-time']
			post.publish(request, start_date, start_time, post.status)
			return redirect('raportowanie:post_filled', post_id=post.id)
	else:
		form = PostForm()
	content = {
		"login_user": logged_user(request),
		"view_type_hyperlink": "../../",
		'form': form,
		"date": str(timezone.now().date()),
		"time": str(timezone.now().time())[0:5],
		"view_type": "Nowe zgłoszenie",
		"name_of_form": "Formularz tworzenia zgloszenia"

	}
	return render(request, 'aplikacja_raportowanie/post_new.html', content)

#Funkcja do edycji obenego zgłoszenia
@login_required(login_url="/login/")
def post_edit(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		return handler404(request,None)
	post_first_status = post.status
	start_date_split_list = str(post.start_date).split(" ") #dzielimy start_date na date i czas
	date_ = start_date_split_list[0]  #uzyskujemy samą date, a 'date' w pliku html to value inuta date
	time = start_date_split_list[1][0:5] #uzyskujemy samą godzine, a 'time' w pliku html to value inuta time
	if request.method == "POST":
		form = PostForm(request.POST,request.FILES, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			start_date = str(request.POST["post-start-date"]) + ' ' + 	str(request.POST["post-start-time"])
			change = status_change_field(post_first_status, post.status, "Edycja, zamknięcie", "Edycja, ponowne otwarcie", "Edycja", "Otwarcie, do podjęcia", "Podjęcie zgłoszenia")
			post_new_status = f"Edytuje zgłoszenie, {post.status}"
			comment = Comment(text="Edytuje zgłoszenie", publish_date = timezone.now(), status=post_new_status, author=logged_user(request))
			comment.save()
			comment.post_id.add(post.id)
			post.edit(start_date, change, post.status)
			return redirect('raportowanie:post_filled', post_id=post.id)
	else:
		form = PostForm(instance=post)
	content = {
		"login_user": logged_user(request),
		"view_type_hyperlink": "../" + str(post.id),
		"view_type": "Modyfikacja zgloszenia nr. " + str(post.id),
		"back_to_post": "Zgłoszenie nr. "+ str(post.id),
		'form': form,
		"date": date_,
		"time": time,
		"post_id": post_id,
		"name_of_form": "Fromularz edycji zgłoszenia " + str(post.id)
	}
	return render(request, 'aplikacja_raportowanie/post_new.html', content)



#Funkcja pozwalająca zmianę właściciela posta
@login_required(login_url="/login/")
def author_post_change(request, post_id):
	if request.method == "POST":
		new_post_author = request.POST['new-author-of-post']

		try:
			post = Post.objects.get(id=post_id)
		except Post.DoesNotExist:
			return handler404(request,None)
		old_author = post.author

		if old_author:
			comment_status = "ZMIANA WŁAŚCICIELA Z @" + str(old_author) + " NA @"  + str(new_post_author)
			change = "Zmiana właściciela"
		else:
			comment_status = "Ustawiono właściciela na @" + str(new_post_author)
			change = "Ustawienie właściciela"

		post.author_change(new_post_author, change)
		comment = Comment(text=str(request.POST['comment-text-after-author-edit']), publish_date=timezone.now(), status=comment_status, author=logged_user(request))
		comment.save()
		comment.post_id.add(post.id)
		return redirect('raportowanie:post_filled', post_id=post.id)
	else:
		return redirect('raportowanie:post_filled', post_id)




#Funkcja pozwalająca edycję komentarza
@login_required(login_url="/login/")
def comment_edit(request, post_id, comment_id):
	try:
		post = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		return handler404(request,None)
	comment = Comment.objects.get(id = comment_id)
	if request.method == "POST":
		form = CommentForm(request.POST, request.FILES, instance=comment)
		if form.is_valid():
			comment = form.save(commit = False)
			comment.edit()
			post_first_status = post.status
			if post.status != comment.status:
				post.modify_date = timezone.now()
			post.status = comment.status
			post.change = status_change_field(post_first_status, post.status, f"Edycja komentarza {comment.id}, zamknięcie", f"Edycja komentarza {comment.id}, ponowne otwarcie", f"Edycja komentarza {comment.id}", f"Edycja koentarza {comment.id}, otwarcie, do podjęcia", f'Podjęcie zgłoszenia')
			post.save()
			return redirect('raportowanie:post_filled', post_id = post_id)
	else:
		form = CommentForm(instance=comment)

	content = {
		"login_user": logged_user(request),
		"view_type_hyperlink": "../../" + str(post_id),
		'form': form,
		"view_type": "Edycja komentarza",
		"back_to_post": "Zgłoszenie nr. "+ str(post_id),
		"post_id": post_id,
		'post': post
	}
	return render(request, 'aplikacja_raportowanie/comment_edit.html', content)


def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('raportowanie:index')
	else:
		form = AuthenticationForm()
	return render(request, 'aplikacja_raportowanie/login.html', {'form':form})


def logout_view(request):
	if request.method == "POST":
		logout(request)
		return redirect('raportowanie:login')

def handler404(request, exception):
	return page_not_found(request, exception, template_name="aplikacja_raportowanie/404.html")
