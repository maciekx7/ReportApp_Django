from aplikacja_raportowanie.liblaries import *

from aplikacja_raportowanie.models import STATUS_CHOICES



FIRST_YEAR_IN_QUATER_SORT = 2012
APPLICATION_START_DATE = "2019-09-02"
STATUS_CHOICES_LIST_WITHOUT_CLOSE = [element[0] for element in STATUS_CHOICES[0:len(STATUS_CHOICES)-1]]
STATUS_CHOICES_LIST_WITH_CLOSE = [element[0] for element in STATUS_CHOICES]


#zwraca zalogowanego użytkownika
def logged_user(request):
    return request.user

#zwraca listę użytkowników zarejestrowanych w aplikacji
def list_of_users():
    return User.objects.all()

#zwraca dzisiejszą datę
def todays_date():
    return date.today()

#zwraca listę lat od wybrajen wartości do dzisiejszego roku
def years_list_to_now():
    years = []
    date = int(str(timezone.now().date())[0:4])+1
    for year in range(FIRST_YEAR_IN_QUATER_SORT, date):
    	years.append(year)
    return years

#Zwraca kolor statusu w zgłoszeniu
def status_colors(post):
    if post.status == "zamknięte":
        return "red"
    elif post.status == "przekazane":
        return "orange"
    else:
        return "green"

#uzupełnia zawartość pola, które mówi co użytkownik zmienił
def status_change_field(post_first_status,post_status, if_first, if_second, if_else, if_third, if_last):
    if post_first_status == "do podjęcia" and post_status != "do podjęcia" and post_status != "zamknięte":
        return if_last
    if post_first_status != "zamknięte" and post_status == "zamknięte":
        return if_first
    elif post_first_status == "zamknięte" and post_status == "do podjęcia":
        return if_third
    elif post_first_status == "zamknięte" and post_status != "zamknięte":
    	return if_second
    else:
    	return if_else


#zwraca listę zdarzeń w kwartale z ustalonym filtrowaniem statusu i użytkownika
def which_quater(request, quater, status_, author_, what_, date_type):
    if date_type == "publish_date":
        if author_ == "wszyscy":
            return Post.objects.filter(is_deleted=False, status__in = status_, publish_date__range=(quater))
        else:
            if what_ == "jestem_wlascicielem":
                return Post.objects.filter(author = User.objects.get(username=author_), status__in = status_, is_deleted = False, publish_date__range=(quater))
            elif what_ == "jestem-bylem_wlascicielem":
                list_of_posts = []
                for post in Post.objects.filter(status__in = status_, is_deleted = False, publish_date__range=(quater)):
                    for post_history in post.history.all():
                        if str(post_history.author) == str(author_):
                            list_of_posts.append(Post.objects.get(id=post.id))
                            break
                return list_of_posts
            elif what_ == "skomentowałem":
                list_of_posts = []
                for post in Post.objects.filter(status__in = status_, is_deleted = False, publish_date__range=(quater)):
                    for comment in Comment.objects.filter(post_id = post):
                        if str(comment.author) == str(author_):
                            list_of_posts.append(post)
                            break
                return list_of_posts
    elif date_type == "modify_date":
        if author_ == "wszyscy":
            return Post.objects.filter(is_deleted=False, status__in = status_, modify_date__range=(quater))
        else:
            if what_ == "jestem_wlascicielem":
                return Post.objects.filter(author = User.objects.get(username=author_), status__in = status_, is_deleted = False, modify_date__range=(quater))
            elif what_ == "jestem-bylem_wlascicielem":
                list_of_posts = []
                for post in Post.objects.filter(status__in = status_, is_deleted = False, modify_date__range=(quater)):
                    for post_history in post.history.all():
                        if str(post_history.author) == str(author_):
                            list_of_posts.append(Post.objects.get(id=post.id))
                            break
                return list_of_posts
            elif what_ == "skomentowałem":
                list_of_posts = []
                for post in Post.objects.filter(status__in = status_, is_deleted = False, modify_date__range=(quater)):
                    for comment in Comment.objects.filter(post_id = post):
                        if str(comment.author) == str(author_):
                            list_of_posts.append(post)
                            break
                return list_of_posts
    elif date_type == "start_date":
        if author_ == "wszyscy":
            return Post.objects.filter(is_deleted=False, status__in = status_, start_date__range=(quater))
        else:
            if what_ == "jestem_wlascicielem":
                return Post.objects.filter(author = User.objects.get(username=author_), status__in = status_, is_deleted = False, start_date__range=(quater))
            elif what_ == "jestem-bylem_wlascicielem":
                list_of_posts = []
                for post in Post.objects.filter(status__in = status_, is_deleted = False, start_date__range=(quater)):
                    for post_history in post.history.all():
                        if str(post_history.author) == str(author_):
                            list_of_posts.append(Post.objects.get(id=post.id))
                            break
                return list_of_posts
            elif what_ == "skomentowałem":
                list_of_posts = []
                for post in Post.objects.filter(status__in = status_, is_deleted = False, start_date__range=(quater)):
                    for comment in Comment.objects.filter(post_id = post):
                        if str(comment.author) == str(author_):
                            list_of_posts.append(post)
                            break
                return list_of_posts

def quater_string(date):
    year = date[0][0:4]
    if date == (f'{year}-01-01', f'{year}-03-31'):
        return f"Filtr po kwartale: I kwartał {year}"
    elif date == (f'{year}-04-01', f'{year}-06-30'):
        return f"Filtr po kwartale: II kwartał {year}"
    elif date == (f'{year}-07-01', f'{year}-09-30'):
        return f"Filtr po kwartale: III kwartał {year}"
    elif date == (f'{year}-10-01', f'{year}-12-31'):
        return f"Filtr po kwartale: IV kwartał {year}"
    elif date == (f'{year}-01-01', f'{year}-06-30'):
        return f"Filtr po półroczu: I połrocze {year}"
    elif date == (f'{year}-07-01', f'{year}-12-31'):
        return f"Filtr po półroczu: II połrocze {year}"
    else:
        return "Filtr okresowy: " + str(date)

def status_name_filter(status):
    if status == str(STATUS_CHOICES_LIST_WITH_CLOSE):
        return "wszystkie"
    elif status == str(STATUS_CHOICES_LIST_WITHOUT_CLOSE):
        return "otwarte"
    else:
        return str(status)


#Zwraca listę postów zależną od wybranego widoku
def which_index_view(request, which_view):
    if which_view == "posts_to_do":
        return Post.objects.filter(is_deleted=False, status="do podjęcia")

    if which_view == "user_index":
    	return Post.objects.filter(author=request.user, is_deleted = False, long_term = False).exclude(status__in=["zamknięte", "do podjęcia"]).order_by('-id')
    elif which_view == "index":
    	return Post.objects.filter(is_deleted = False, long_term = False).exclude(status__in=["zamknięte", "do podjęcia"]).order_by('-id')
    elif which_view == "users_index_closed":
    	return Post.objects.filter(status="zamknięte", author = request.user, long_term = False).order_by('-publish_date').exclude(is_deleted = True)
    elif which_view == "index_closed":
    	return Post.objects.filter(status="zamknięte", long_term = False).order_by('-publish_date').exclude(is_deleted = True)
    elif which_view == "index_deleted":
    	return Post.objects.filter(is_deleted = True, long_term = False).order_by('-publish_date')
    elif which_view == "long_index":
        return Post.objects.filter(is_deleted=False, long_term = True)
